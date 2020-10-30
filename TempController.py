import glob
import time
import gpiozero


class TempController:

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    def __init__(self, target, heater_pin, sensor_pin, p=1, i=1, d=1):
        self.target = target
        self.heater_pin = heater_pin
        self.init_heater()       

    def init_heater(self):
        self.heater = gpiozero.PWMOutputDevice(self.heater_pin)

    def update(self):
        temp = self.read_temp()
        print('temp is:')
        print(temp)
        if temp > self.target :
            print('not heating')
            self.heater.off()
        if temp < self.target :
            print('heating on')
            self.heater.value = 100
            self.heater.on()

    def read_temp(self):
        lines = self.read_temp_raw()
        print(lines)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

