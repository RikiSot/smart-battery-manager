import requests
import pandas as pd
from datetime import datetime


def get_irradiance_next_hour():
    # API  parametros
    baseurl = 'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/'
    location_key = '310683'
    apikey = 'LnWxHm4PG1A3A1u2EewGIamqOcUGoxwH'

    parameters = {
        'apikey': apikey,
        'details': 'true'
    }

    url = baseurl + location_key
    response = requests.get(url, params=parameters)
    try:
        result = response.json()[0]['SolarIrradiance']['Value']
    except:
        result = 0
    return result


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    dff = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(dff.shift(i))
        names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(dff.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


# Write to csv
def write_to_csv_RT(filename, names, data):
    print('writing onto csv file at: ', datetime.now())
    filepath = "../Data/" + filename

    df_to_csv = pd.DataFrame(columns=names)
    ts = datetime.now()

    new_row = pd.DataFrame([data], columns=names, index=[ts])
    df_to_csv = pd.concat([df_to_csv, pd.DataFrame(new_row)], ignore_index=False)
    df_to_csv.index.name = 'timeStamp'
    df_to_csv.to_csv(filepath, mode='a', header=False)
