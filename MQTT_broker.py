import sqlite3
import paho.mqtt.client as mqtt
import time
from Sensor_manager import SensorManager

# Configuration
MQTT_BROKER = "localhost"
MQTT_TOPIC_ALL = "sensors/data"
DATABASE_FILE = 'sensors.db'

def insert_data(conn, cursor, temperature, humidity, moisture, probe_temperature):
    try:
        cursor.execute("INSERT INTO sensors (temp_c, humidity, moisture, probe_t) VALUES (?, ?, ?, ?)",
                       (temperature, humidity, moisture, probe_temperature))
        conn.commit()
    except Exception as e:
        print(f"Error inserting data into the database: {str(e)}")

def publish_data(broker, topic, temperature, humidity, moisture, probe_temperature):
    try:
        client = mqtt.Client()
        client.connect(broker, 1883, 60)
        
        # Publish all sensor data as a tuple to the specified topic
        all_data = (temperature, humidity, moisture, probe_temperature)
        client.publish(topic, f"{all_data}")
        
        # Publish human-readable data
        human_readable_message = f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Moisture: {moisture:.2f}%, Probe Temperature: {probe_temperature:.2f}°C"
        client.publish(topic + "/human_readable", human_readable_message)
        #print(topic + "/human_readable)")  
        client.disconnect()
    except Exception as e:
        print(f"Error publishing sensor data to MQTT: {str(e)}")

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
                probe_temperature = latest_data['probe_temperature']

                print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Moisture: {moisture:.2f}%, Probe Temperature: {probe_temperature:.2f}°C")

                insert_data(conn, cursor, temperature, humidity, moisture, probe_temperature)
                
                # Publish data
                publish_data(MQTT_BROKER, MQTT_TOPIC_ALL, temperature, humidity, moisture, probe_temperature)
            else:
                print("Failed to retrieve data from sensors")

            time.sleep(2)  # Read data every 2 seconds

    except KeyboardInterrupt:
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    main()

