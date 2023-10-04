import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import sqlite3
import time

class SensorManager:
    def __init__(self):
        self.setup_DHT()
        self.setup_MCP()

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

    def read_DHT_sensor_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        return humidity, temperature

    def map_analog_to_moisture(self, analog_value, analog_min=175, analog_max=1023):
        # Function to map analog value to moisture level
        moisture_min = 0 # ALWAYS This is the case
        moisture_max = 100 # ALWAYS This is the case
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

    def insert_data(self, temperature, humidity, moisture):
        try:
            conn = sqlite3.connect('sensors.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sensors (temp_c, humidity, moisture) VALUES (?, ?, ?)", (temperature, humidity, moisture))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error inserting data into the database: {str(e)}")

    def get_latest_data(self):
        humidity, temperature = self.read_DHT_sensor_data()
        moisture = self.get_moisture()
        return {
                'temperature': temperature,
                'humidity': humidity,
                'moisture': moisture
                }
    def print_latest_data(self):
        data = self.get_latest_data()
        temperature = data.get('temperature', 'Unable to get Temperature')
        humidity = data.get('humidity', 'Unable to get Humidity')
        moisture = data.get('moisture', 'Unable to get Moisture')

        print(f"Latest Data - Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Moisture: {moisture:.2f}%")



if __name__ == "__main__":
    sensor_manager = SensorManager()
    while True:
        sensor_manager.print_latest_data()
        time.sleep(5)
