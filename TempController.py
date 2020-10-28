import glob
import time
import RPi.GPIO as GPIO

from simple_pid import PID

class TempController:

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    cycle_time = 1  # cycle time in seconds
    frequency = 1000  # pwm frequency

    def __init__(self, target, heater_pin, sensor_pin, p=1, i=1, d=1):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.heater_pin, GPIO.OUT)
        self.pid = PID(p, i, d, setpoint=target)
        self.pid.sample_time = self.cycle_time
        self.heater_pin = heater_pin
        # self.sensor_pin = sensor_pin

    def __exit__(self, exception_type, exception_value, exception_traceback):
        GPIO.cleanup()

    def __del__(self):
        GPIO.cleanup(self.heater_pin)
        # GPIO.cleanup(self.sensor_pin)

    def update(self):
        value = self.read_temp()
        control = self.pid(value)
        self.apply_control(control)

    def read_temp(self):
        lines = self.read_temp_raw()
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

    def apply_control(self, control):
        heater = GPIO.PWM(self.heater_pin, self.frequency)
        heater.start(max(min(int(control), 100), 0))
        time.sleep(self.cycle_time)
        heater.stop()
