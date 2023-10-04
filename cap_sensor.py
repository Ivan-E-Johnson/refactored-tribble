import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

# MCP3008 setup
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Function to map analog value to moisture level (customize this based on your sensor)
def map_to_moisture(analog_value):
    # Replace these values with the actual min and max values you observe
    analog_min = 175 # Inspection of sensor in water
    analog_max = 1023
    moisture_min = 0  # Corresponding to dry
    moisture_max = 100  # Corresponding to wet

    # Map the analog value to the moisture level
    moisture = (analog_value - analog_min) / (analog_max - analog_min) * (moisture_min - moisture_max) + moisture_max
    print(moisture) 
    return min(moisture, moisture_max)


# Main loop
while True:
    # Read the analog input from the MCP3008
    analog_value = mcp.read_adc(0)
    
    # Map the analog value to moisture level
    moisture = map_to_moisture(analog_value)

    print(f'Analog value: {analog_value}')
    print(f'Moisture level: {moisture}%')

    # Adjust the sleep time based on your requirements
    time.sleep(1)  # Sleep for 1 second before the next reading

