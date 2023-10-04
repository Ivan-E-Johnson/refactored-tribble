import Adafruit_DHT
import time
import sqlite3
import paho.mqtt.client as mqtt
from dht22 import read_sensor_data, setup_DHT
# Configuration
MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensor/dht22"
DATABASE_FILE = 'sensors.db'


# Function to insert data into the database
def insert_data(conn, cursor, temperature, humidity):
    try:
        cursor.execute("INSERT INTO sensors (temp_c, humidity) VALUES (?, ?)", (temperature, humidity))
        conn.commit()
    except Exception as e:
        print(f"Error inserting data into the database: {str(e)}")

# Function to publish data to MQTT
def publish_mqtt_data(broker, topic, temperature, humidity):
    try:
        client = mqtt.Client()
        client.connect(broker, 1883, 60)
        message = f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%"
        client.publish(topic, message)
        client.disconnect()
    except Exception as e:
        print(f"Error publishing data to MQTT: {str(e)}")

def main():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        DHT_SENSOR, DHT_PIN = setup_DHT()
        while True:
            humidity, temperature = read_sensor_data(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")
                
                insert_data(conn, cursor, temperature, humidity)
                publish_mqtt_data(MQTT_BROKER, MQTT_TOPIC, temperature, humidity)
                
            else:
                print("Failed to retrieve data from DHT sensor")
            
            time.sleep(2)  # Read data every 2 seconds

    except KeyboardInterrupt:
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    main()

