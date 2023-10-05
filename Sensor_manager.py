import os
import time
import configparser
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import sqlite3

class SensorManager:
    def __init__(self, config_file='config.ini'):
        self.setup_DHT()
        self.setup_MCP()
        self.setup_TemperatureProbe(config_file)

    def setup_DHT(self):
        # DHT22 sensor setup
        self.DHT_SENSOR = Adafruit_DHT.DHT22
        self.DHT_PIN = 17  # Change this to match your GPIO pin

    def setup_MCP(self):
        # MCP3008 setup
        CLK = 18
        MISO = 23
        MOSI = 24
        CS = 25
        self.mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

    def setup_TemperatureProbe(self, config_file):
        self.temperature_probe = TemperatureProbe(config_file)

    def read_DHT_sensor_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        return humidity, temperature

    def map_analog_to_moisture(self, analog_value, analog_min=175, analog_max=1023):
        # Function to map analog value to moisture level
        moisture_min = 0  # ALWAYS This is the case
        moisture_max = 100  # ALWAYS This is the case
        moisture = moisture_max - ((analog_value - analog_min) / (analog_max - analog_min) * (moisture_max - moisture_min) + moisture_min)
        moisture = max(moisture_min, moisture)  # Ensure we don't get negative values
        moisture = min(moisture_max, moisture)

        return moisture

    def read_analog_value(self):
        # Read the analog input from the MCP3008
        return self.mcp.read_adc(0)

    def get_moisture(self):
        analog_val = self.read_analog_value()
        moisture = self.map_analog_to_moisture(analog_val)
        return moisture

    def insert_data(self, temperature, humidity, moisture, probe_temperature):
        try:
            conn = sqlite3.connect('sensors.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sensors (temp_c, humidity, moisture, probe_temperature) VALUES (?, ?, ?, ?)",
                           (temperature, humidity, moisture, probe_temperature))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error inserting data into the database: {str(e)}")

    def get_latest_data(self):
        humidity, temperature = self.read_DHT_sensor_data()
        moisture = self.get_moisture()
        probe_temperature = self.temperature_probe.read_temp()
        return {
            'temperature': temperature,
            'humidity': humidity,
            'moisture': moisture,
            'probe_temperature': probe_temperature
        }

    def print_latest_data(self):
        data = self.get_latest_data()
        temperature = data.get('temperature', 'Unable to get Temperature')
        humidity = data.get('humidity', 'Unable to get Humidity')
        moisture = data.get('moisture', 'Unable to get Moisture')
        probe_temperature = data.get('probe_temperature', 'Unable to get Probe Temperature')

        print(f"Latest Data - Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Moisture: {moisture:.2f}%, Probe Temperature: {probe_temperature:.2f}°C")


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
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c


if __name__ == "__main__":
    sensor_manager = SensorManager()
    while True:
        sensor_manager.print_latest_data()
        time.sleep(5)

