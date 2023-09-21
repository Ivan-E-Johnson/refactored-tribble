import Adafruit_DHT
import time
import sqlite3

# Set the GPIO pin you connected the DHT22 data pin to
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 3  # Change this to match your GPIO pin

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

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")
            
            # Insert data into the database
            insert_data(temperature, humidity)
            
        else:
            print("Failed to retrieve data from DHT sensor")
        time.sleep(2)  # Read data every 2 seconds

except KeyboardInterrupt:
    pass

