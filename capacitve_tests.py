import RPi.GPIO as GPIO
import time

# Set the GPIO mode and channel
GPIO.setmode(GPIO.BCM)
moisture_pin = 4  # Change this to the GPIO pin you used for the analog output

# Setup the channel as an input
GPIO.setup(moisture_pin, GPIO.IN)

try:
    while True:
        # Read the moisture level
        moisture_level = GPIO.input(moisture_pin)
        print(f"Moisture Level: {moisture_level}")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

