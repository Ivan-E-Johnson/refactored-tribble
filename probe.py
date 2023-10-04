import os
import time
import configparser

class TemperatureProbe:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.device_file = self.config.get('Sensor', 'device_file')
        
    def read_temp_raw(self):
        with open(self.device_file, 'r') as f:
            lines = f.readlines()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

if __name__ == "__main__":
    sensor = TemperatureProbe('config.ini')  # Use a configuration file for device-specific settings

    while True:
        temp_c = sensor.read_temp()
        print(temp_c)
        time.sleep(1)

