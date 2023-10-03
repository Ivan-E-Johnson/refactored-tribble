import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import datetime
import time

# MCP3008 setup
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Setting up parameters for effecting the functionality of the code
debounce_time = 0.5
analog_threshold = 50

# Main loop
while True:
    time.sleep(debounce_time)
    # Read the analog input from the MCP3008
    analog_value = mcp.read_adc(0)
    print(f'analog {analog_value}')
    print(f"difference {mcp.read_adc_difference(0)}")

