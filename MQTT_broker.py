import sqlite3
import paho.mqtt.client as mqtt
import time
from Sensor_manager import SensorManager

# Configuration
MQTT_BROKER = "localhost"
MQTT_TOPIC_DHT22 = "sensor/dht22"
MQTT_TOPIC_PROBE = "sensor/temperature_probe"
MQTT_TOPIC_ALL = "sensors/data"
DATABASE_FILE = 'sensors.db'

def insert_data(conn, cursor, temperature, humidity, moisture, probe_temperature):
    try:
        cursor.execute("INSERT INTO sensors (temp_c, humidity, moisture, probe_temperature) VALUES (?, ?, ?, ?)",
                       (temperature, humidity, moisture, probe_temperature))
        conn.commit()
    except Exception as e:
        print(f"Error inserting data into the database: {str(e)}")

def publish_individual_sensor_data(broker, dht22_topic, probe_topic, temperature, humidity, moisture, probe_temperature):
    try:
        client = mqtt.Client()
        client.connect(broker, 1883, 60)
        
        # Publish DHT22 data to its topic
        dht22_message = f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Moisture: {moisture:.2f}%"
        client.publish(dht22_topic, dht22_message)
        
        # Publish Temperature Probe data to its topic
        probe_message = f"Probe Temperature: {probe_temperature:.2f}°C"
        client.publish(probe_topic, probe_message)
        
        client.disconnect()
    except Exception as e:
        print(f"Error publishing individual sensor data to MQTT: {str(e)}")

def publish_all_sensor_data(broker, all_topic, temperature, humidity, moisture, probe_temperature):
    try:
        client = mqtt.Client()
        client.connect(broker, 1883, 60)
        
        # Publish all sensor data as a tuple to the "sensors/data" topic
        all_data = (temperature, humidity, moisture, probe_temperature)
        all_message = f"Sensor Data: {all_data}"
        client.publish(all_topic, all_message)
        
        client.disconnect()
    except Exception as e:
        print(f"Error publishing all sensor data to MQTT: {str(e)}")

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
                
                # Publish individual sensor data
                publish_individual_sensor_data(MQTT_BROKER, MQTT_TOPIC_DHT22, MQTT_TOPIC_PROBE, temperature, humidity, moisture, probe_temperature)
                
                # Publish all sensor data as a tuple
                publish_all_sensor_data(MQTT_BROKER, MQTT_TOPIC_ALL, temperature, humidity, moisture, probe_temperature)
            else:
                print("Failed to retrieve data from sensors")

            time.sleep(2)  # Read data every 2 seconds

    except KeyboardInterrupt:
        pass
    finally:
        conn.close()

if __name__ == "__main__":
    main()

