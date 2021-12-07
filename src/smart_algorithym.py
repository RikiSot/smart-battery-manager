# Imports
import pickle
import random

import keras
import numpy as np


from bateria import Bateria
from functions import *


class SmartAlgorithym():

    def __init__(self):
        self.bateria = Bateria()
        # Load model
        self.model = keras.models.load_model('..\Data\consumos_model.h5')
        # Load scaler
        self.scaler = pickle.load(open('..\Data\scaler.pkl', 'rb'))
        # Ruta del csv
        self.filepath = '..\Data\household_power_consumption.txt'
        # Numero de horas de la ventana temporal
        self.n_hours = 24
        # Superficie de paneles instalados en m2
        self.sup_paneles = 17
        # Rendimiento de los paneles en base 1
        self.rendimiento = 0.15
        # Coef seguridad en la comparacion
        self.x_security = 1.5
        # Next forecast irradiation
        self.irradiance = get_irradiance_next_hour()

        # Posicion inicial de lectura en el df. Testing purposes
        self.is_df_randomized = 0

    def is_valley(self):
        # Periodo valle. Indica que hay que cargar independientemente del resto
        fecha = datetime.today()
        hora = fecha.hour
        dia_semana = fecha.weekday()

        if (hora >= 0 and hora < 8):
            return 1
        else:
            return 0

        # Posibilidad de incluir sábados y domingos

        # if ((hora >= 0 and hora < 8) or (dia_semana > 4 and dia_semana <= 6)):
        #     return 1
        # else:
        #     return 0

    def charge_battery_night(self):
        # print('Checkeando si es valley a las: ',datetime.now())
        if (self.is_valley()):
            if (self.bateria.battery_level <= self.bateria.max_level_night):
                # Cargar independientemente del consumo
                self.bateria.cargar_bateria = 1
            # Cargar hasta que el porcentaje de bateria llega al maximo establecido
            else:
                self.bateria.cargar_bateria = 0
            write_to_csv_RT('../Data/charge_battery_data.csv', ['charge_battery', 'consumo', 'generation'],
                            [self.bateria.cargar_bateria, 'NaN', 'NaN'])

    def make_prediction(self, data):
        yhat = self.model.predict(data)
        # Invertir el escalado de la predicción
        try:
            inv_yhat = np.concatenate((yhat, self.scaled_last_row), axis=1)
            inv_yhat = self.scaler.inverse_transform(inv_yhat)
            inv_yhat = inv_yhat[:, 0]
            return inv_yhat[0]
        except:
            print('Called before adapt_data. No scaled data')

    def load_data(self):
        # Lectura del archivo (prueba con el dataset)
        df = pd.read_csv(self.filepath, sep=';',
                         parse_dates={'Fecha': ['Date', 'Time']},
                         infer_datetime_format=True,
                         low_memory=False,
                         na_values=['nan', '?'],
                         index_col='Fecha')
        return df

    def adapt_data(self, df):

        # Tratamiento de NaN
        df = df.interpolate()
        df.isnull().sum()

        # Eliminar voltaje y energia reativa
        df = df.drop(['Voltage', 'Global_reactive_power'], axis=1)

        # Cambio de unidades a KWh
        df['Sub_metering_1'] = df['Sub_metering_1'] / 1000
        df['Sub_metering_2'] = df['Sub_metering_2'] / 1000
        df['Sub_metering_3'] = df['Sub_metering_3'] / 1000

        # Cambio de potencia a energia (kWh)
        df['Energia activa global'] = df['Global_active_power'] / 60

        # Medidor 4
        df['Sub_metering_4'] = df['Energia activa global'] - (
                    df['Sub_metering_1'] + df['Sub_metering_2'] + df['Sub_metering_3'])

        # Creacion del nuevo dataframe
        df_mean = df[['Global_intensity']].copy()
        df_sum = df.drop(['Global_intensity', 'Global_active_power'], axis=1)

        # Resampling del nuevo dataframe
        df_mean = df_mean.resample('h').mean()
        df_sum = df_sum.resample('h').sum()

        df1 = df_mean.merge(df_sum, left_index=True, right_index=True)

        # Mover energia activa a la ultima posicion
        brb = df1.pop('Energia activa global')  # remove column b and store it in brb
        df1.insert(0, 'Energia activa global', brb)  # en primera posicion

        # Únicamente interesan las últimas 24 horas
        n_features = df1.shape[1]

        # Seleccion de los valores de la ultimas 24h
        df1 = df1.tail(self.n_hours)

        # Escalado
        values = df1.values
        scaled = self.scaler.transform(values)

        # Para deshacer el escalado despues
        self.scaled_last_row = scaled[-1:, 1:]

        # Series to supervised
        data_to_model = series_to_supervised(scaled, self.n_hours - 1, 1)

        # Redimensionar el input a 3d [muestras, secuencias, variables]
        data_to_model = data_to_model.values.reshape((data_to_model.values.shape[0], self.n_hours, n_features))
        return data_to_model

    # TESTING
    def adapt_data_test(self, df):

        # Tratamiento de NaN
        df = df.interpolate()
        df.isnull().sum()

        # Eliminar voltaje y energia reativa
        df = df.drop(['Voltage', 'Global_reactive_power'], axis=1)

        # Cambio de unidades a KWh
        df['Sub_metering_1'] = df['Sub_metering_1'] / 1000
        df['Sub_metering_2'] = df['Sub_metering_2'] / 1000
        df['Sub_metering_3'] = df['Sub_metering_3'] / 1000

        # Cambio de potencia a energia (kWh)
        df['Energia activa global'] = df['Global_active_power'] / 60

        # Medidor 4
        df['Sub_metering_4'] = df['Energia activa global'] - (
                    df['Sub_metering_1'] + df['Sub_metering_2'] + df['Sub_metering_3'])

        # Creacion del nuevo dataframe
        df_mean = df[['Global_intensity']].copy()
        df_sum = df.drop(['Global_intensity', 'Global_active_power'], axis=1)

        # Resampling del nuevo dataframe
        df_mean = df_mean.resample('h').mean()
        df_sum = df_sum.resample('h').sum()

        df1 = df_mean.merge(df_sum, left_index=True, right_index=True)

        # Mover energia activa a la ultima posicion
        brb = df1.pop('Energia activa global')  # remove column b and store it in brb
        df1.insert(0, 'Energia activa global', brb)  # en primera posicion

        # Únicamente interesan las últimas 24 horas
        n_features = df1.shape[1]

        # Seleccionar punto de partida aleatorio en el dataset. Misma hora, dia aleatorio

        # Seleccion de valor random. Una vez por ejecucion
        if (self.is_df_randomized == 0):
            self.is_df_randomized = 1
            # Conseguir indice del dia aleatorio
            df2 = df1.copy()
            df2['hour'] = df2.index.hour
            df2 = df2.reset_index()
            # Mask de todos los puntos con la misma hora
            df2 = df2.loc[df2.hour == datetime.now().hour]
            random_first_index = random.randint(25, len(df2) - 25)
            # Equivalencia de indice en el df original
            self.starting_indice = df2.iloc[random_first_index].name

        # Recortar dataframe al minimo requerido
        df1 = df1.iloc[self.starting_indice - 24:self.starting_indice]

        # Aumentar indice para siguiente iteracion
        self.starting_indice += 1

        # Escalado
        values = df1.values
        scaled = self.scaler.transform(values)

        # Para deshacer el escalado despues
        self.scaled_last_row = scaled[-1:, 1:]

        # Series to supervised
        data_to_model = series_to_supervised(scaled, self.n_hours - 1, 1)

        # Redimensionar el input a 3d [muestras, secuencias, variables]
        data_to_model = data_to_model.values.reshape((data_to_model.values.shape[0], self.n_hours, n_features))
        return data_to_model

    def compare_power(self, consumo, generacion):
        # Estados independientes de la comparacion:
        if (self.bateria.battery_level >= self.bateria.max_level_day):
            self.bateria.cargar_bateria = 0
        elif (self.bateria.battery_level <= self.bateria.min_level_day):
            self.bateria.cargar_bateria = 1

        elif (generacion < consumo * self.x_security):
            self.bateria.cargar_bateria = 1
        elif (generacion >= consumo * self.x_security):
            self.bateria.cargar_bateria = 0

    def set_irradiance_next_hour(self):
        self.irradiance = get_irradiance_next_hour()
        print('Update forecasted irradiance. New value for hour ' + str(datetime.now().hour + 1) + ' is: ' + str(
            self.irradiance))

    def power_from_irradiance(self):
        power = self.irradiance * self.rendimiento * (self.sup_paneles / 1000)
        return power

    def bucle_normal(self):
        print()
        print('Entrando en el bucle a las: ', datetime.now())
        if (self.is_valley() == 0):
            # 3. Lectura de datos
            print('Cargando datos del csv a las: ', datetime.now())
            data = self.load_data()

            # 4. Adaptar datos
            data = self.adapt_data(data)

            # 5. Realizar la prediccion
            print('Realizando prediccion a las: ', datetime.now())
            consumo_prediction = self.make_prediction(data)

            # 6. Obtener el valor de la generacion y potencia en la proxima hora
            generation = self.power_from_irradiance()

            # . Comparar ambos valores
            self.compare_power(consumo_prediction, generation)
            write_to_csv_RT('../Data/charge_battery_data.csv', ['charge_battery', 'consumo', 'generation'],
                            [self.bateria.cargar_bateria, consumo_prediction, generation])

    def bucle_test(self):
        print()
        print('Entrando en el bucle a las: ', datetime.now())
        if (self.is_valley() == 0):
            # 3. Lectura de datos
            print('Cargando datos del csv a las: ', datetime.now())
            data = self.load_data()

            # 4. Adaptar datos
            data = self.adapt_data_test(data)

            # 5. Realizar la prediccion
            print('Realizando prediccion a las: ', datetime.now())
            consumo_prediction = self.make_prediction(data)

            # 6. Obtener el valor de la generacion y potencia en la proxima hora
            generation = self.power_from_irradiance()

            # . Comparar ambos valores
            self.compare_power(consumo_prediction, generation)
            write_to_csv_RT('../Data/charge_battery_data.csv', ['charge_battery', 'consumo', 'generation'],
                            [self.bateria.cargar_bateria, consumo_prediction, generation])



