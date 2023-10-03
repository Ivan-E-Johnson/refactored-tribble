import requests
import Adafruit_DHT
import time

SENSOR_PIN = 16  # Change this to match your DHT22 pin
API_URL = 'http://172.17.47.183:8000/api/sensor-readings/'  # Change to your local machine's IP and port

while True:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, SENSOR_PIN)
    
    if humidity is not None and temperature is not None:
        data = {
            'temperature': temperature,
            'humidity': humidity,
        }
        
        response = requests.post(API_URL, data=data)
        
        if response.status_code == 201:
            print('Data sent successfully!')
        else:
            print('Failed to send data.')
    
    time.sleep(60)  # Adjust the interval as needed

