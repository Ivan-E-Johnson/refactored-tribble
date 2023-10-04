import sqlite3
import paho.mqtt.client as mqtt
import time
from sensor_manager import SensorManager

# Configuration
MQTT_BROKER = "localhost"
MQTT_TOPIC = "sensor/dht22"
DATABASE_FILE = 'sensors.db'

def insert_data(conn, cursor, temperature, humidity, moisture):
    try:
        cursor.execute("INSERT INTO sensors (temp_c, humidity, moisture) VALUES (?, ?, ?)", (temperature, humidity, moisture))
        conn.commit()
    except Exception as e:
        print(f"Error inserting data into the database: {str(e)}")

def publish_mqtt_data(broker, topic, temperature, humidity, moisture):
    try:
        client = mqtt.Client()
        client.connect(broker, 1883, 60)
        message = f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Moisture: {moisture:.2f}%"
        client.publish(topic, message)
        client.disconnect()
    except Exception as e:
        print(f"Error publishing data to MQTT: {str(e)}")

def main():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        sensor_manager = SensorManager()

        while True:
            latest_data = sensor_manager.get_latest_data()
            if latest_data:
                temperature = latest_data['temperature']
                humidity = latest_data['humidity']
                moisture = latest_data['moisture']

                print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Moisture: {moisture:.2f}%")

                insert_data(conn, cursor, temperature, humidity, moisture)
                publish_mqtt_data(MQTT_BROKER, MQTT_TOPIC, temperature, humidity, moisture)
            else:
                print("Failed to retrieve data from sensors")

            time.sleep(2)  # Read data every 2 seconds

    except KeyboardInterrupt:
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    main()

