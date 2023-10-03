import RPi.GPIO as GPIO
import time

# Set the GPIO mode and channel
GPIO.setmode(GPIO.BCM)
moisture_pin = 24  # Change this to the GPIO pin you used for the analog output
CS_PIN = 25
# Setup the channel as an input
GPIO.setup(moisture_pin, GPIO.IN)
GPIO.setup(CS_PIN, GPIO.OUT)
# Release the CS pin
GPIO.output(CS_PIN, GPIO.LOW)
try:
    while True:
        GPIO.output(CS_PIN, GPIO.LOW)
        # Read the moisture level
        moisture_level = GPIO.input(moisture_pin)
        print(f"Moisture Level: {moisture_level}")
        time.sleep(1)
        # Release the CS pin
        GPIO.output(CS_PIN, GPIO.HIGH)
except KeyboardInterrupt:
    GPIO.cleanup()

