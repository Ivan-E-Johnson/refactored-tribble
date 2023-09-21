import Adafruit_DHT
import time

# Set the GPIO pin you connected the DHT22 data pin to
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 3  # Change this to match your GPIO pin

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")
        else:
            print("Failed to retrieve data from DHT sensor")
        time.sleep(2)  # Read data every 2 seconds

except KeyboardInterrupt:
    pass

