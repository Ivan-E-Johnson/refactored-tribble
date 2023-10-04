import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

# Function to set up MCP3008
def setup_MCP(clk_pin, miso_pin, mosi_pin, cs_pin):
    return Adafruit_MCP3008.MCP3008(clk=clk_pin, cs=cs_pin, miso=miso_pin, mosi=mosi_pin)

# Function to map analog value to moisture level
def map_to_moisture(analog_value, analog_min=175, analog_max=1023):
    
    moisture_min = 0 # ALWAYS This is the case
    moisture_max = 100 # ALWAYS This is the case

    # Reverse the mapping: 0% moisture when submerged in water, 100% moisture when dry
    moisture = moisture_max - ((analog_value - analog_min) / (analog_max - analog_min) * (moisture_max - moisture_min) + moisture_min)
    #print(moisture)
    moisture = max(moisture_min, moisture)  # Ensure we don't get negative values
    #print(moisture)
    moisture = min(moisture_max, moisture) 
    #print(moisture)
    
    return moisture
def read_analog_value(mcp):
    # Read the analog input from the MCP3008
    return mcp.read_adc(0)

def get_moisture(mcp):
    analog_val = read_analog_value(mcp)
    moisture = map_to_moisture(analog_val)
    return moisture


def main():
    # MCP3008 setup
    CLK = 18
    MISO = 23
    MOSI = 24
    CS = 25
    mcp = setup_MCP(CLK, MISO, MOSI, CS)

    # Main loop
    while True:
        # Read the analog input from the MCP3008
        analog_value = read_analog_value(mcp)

        # Map the analog value to moisture level
        moisture = map_to_moisture(analog_value, analog_max=500)

        print(f'Analog value: {analog_value}')
        print(f'Moisture level: {moisture}%')

        # Adjust the sleep time based on your requirements
        time.sleep(1)  # Sleep for 1 second before the next reading

if __name__ == "__main__":
    main()

