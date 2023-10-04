import Adafruit_DHT
import time
import sqlite3
#import rpi.GPIO as GPIO
# Set the GPIO pin you connected the DHT22 data pin to
DHT_SENSOR = Adafruit_DHT.DHT22

DHT_PIN = 17  # Change this to match your GPIO pin

# Function to insert data into the database
def insert_data(temperature, humidity):
    try:
        conn = sqlite3.connect('temperature.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO temperature (temp_c, humidity) VALUES (?, ?)", (temperature, humidity))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error inserting data into the database: {str(e)}")

def setup_DHT():
    # DHT22 sensor setup
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 17  # Change this to match your GPIO pin
    return DHT_SENSOR, DHT_PIN # is this useful?


# Function to read sensor data
def read_sensor_data(DHT_SENSOR,DHT_PIN):
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity, temperature

if __name__ == '__main__':
    try:
        DHT_SENSOR, DHT_PIN = setup_DHT()
        while True:
            humidity, temperature = read_sensor_data(DHT_SENSOR, DHT_PIN) 
            if humidity is not None and temperature is not None:
                print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")
            
                # Insert data into the database
                # insert_data(temperature, humidity)
            
            else:
                print("Failed to retrieve data from DHT sensor")
            time.sleep(2)  # Read data every 2 seconds

    except KeyboardInterrupt:
        pass

