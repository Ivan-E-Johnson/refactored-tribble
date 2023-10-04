import os
import sqlite3
import socket
import time




device_file = '/sys/bus/w1/devices/28-3c80e3819f89/w1_slave'  # path to the device file that stores temperature data



# Function to read the raw temperature data from the device file
def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines


# Function to parse the temperature value from the device file
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0

        return temp_c

while True:
    #display.lcd_clear()
    temp_c = read_temp() 
    print(temp_c)
