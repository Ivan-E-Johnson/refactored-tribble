import Adafruit_DHT
import time
import sqlite3
import paho.mqtt.client as mqtt

# DHT22 sensor setup
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17  # Change this to match your GPIO pin

# MQTT settings
MQTT_BROKER = "localhost"  # Change to the IP or hostname of your MQTT broker
MQTT_TOPIC = "sensor/dht22"

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

# Function to publish data to MQTT
def publish_mqtt_data(temperature, humidity):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, 1883, 60)
    message = f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%"
    client.publish(MQTT_TOPIC, message)
    client.disconnect()

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")
            
            # Insert data into the database
            insert_data(temperature, humidity)
            
            # Publish data to MQTT
            publish_mqtt_data(temperature, humidity)
            
        else:
            print("Failed to retrieve data from DHT sensor")
        time.sleep(2)  # Read data every 2 seconds

except KeyboardInterrupt:
    pass

