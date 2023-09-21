import socket
import time
import random

# Define the server's IP address and port
server_address = ('172.17.30.81', 4000)

# Create a socket and connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)

while True:
    # Generate a random temperature between 20 and 30 degrees Celsius
    temperature = random.uniform(20.0, 30.0)
    # Format the data as a string
    data = "Temperature: {:.1f}C".format(temperature)
    # Send the data to the server
    sock.sendall(data.encode('utf-8'))
    # Wait for 10 seconds before sending the data again
    time.sleep(1)


