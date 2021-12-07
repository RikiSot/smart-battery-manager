class Bateria():

    def __init__(self):
        self.battery_level = 50
        self.max_level_night = 85
        self.cargar_bateria = 0
        self.max_level_day = 80
        self.min_level_day = 20

    def charge_simulator(self):
        print('Charge simulator')
        if (self.battery_level > 0 and self.battery_level < 100):
            if (self.cargar_bateria == 1):
                self.battery_level += 1
            else:
                self.battery_level -= 1

    def reset(self):
        self.battery_level = 50

    def full_charge(self):
        self.battery_level = 100

    def empty_charge(self):
        self.battery_level = 0