#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import time
import random  # Import the random module

import paho.mqtt.client as paho
from paho import mqtt
from Sensor_manager import SensorManager


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    """
        Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param flags: these are response flags sent by the broker
        :param rc: stands for reasonCode, which is a code for the connection result
        :param properties: can be used in MQTTv5, but is optional
    """
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    """
        Prints mid to stdout to reassure a successful publish ( used as callback for publish )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param properties: can be used in MQTTv5, but is optional
    """
    print(f"published {mid}, {userdata}, {properties}")
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """
        Prints a reassurance for successfully subscribing

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
        :param properties: can be used in MQTTv5, but is optional
    """

    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="TESTING_PUB", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(username="SeniorDesign", password="Sproutsmart")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("0504a46095234ca98948eed4095f98e8.s2.eu.hivemq.cloud", 8883,clean_start=True, keepalive=60)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# # subscribe to all topics of encyclopedia by using the wildcard "#"
# client.subscribe("encyclopedia/#", qos=1)



# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop


def publish_random_number(client, topic):
    random_value = random.randint(0, 100)  # Generate a random number between 0 and 100
    payload = str(random_value)  # Convert the random number to a string

    client.publish(topic, payload=payload, qos=1)  # Publish the random number to the topic
client.loop_start()  # Start the MQTT client

def pub_sensor_data(client, topic, latest_data):
    temperature = latest_data['temperature']
    humidity = latest_data['humidity']
    moisture = latest_data['moisture']
    probe_temperature = latest_data['probe_temperature']
    payload = f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Moisture: {moisture:.2f}%, Probe Temperature: {probe_temperature:.2f}°C"
    client.publish(topic, payload=payload,qos =1 )
sensor_manager = SensorManager()
topic = "sensors/data"
while True:
        
    latest_data = sensor_manager.get_latest_data()
    if latest_data:
        temperature = latest_data['temperature']
        humidity = latest_data['humidity']    
        moisture = latest_data['moisture']
        probe_temperature = latest_data['probe_temperature']
        print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Moisture: {moisture:.2f}%, Probe Temperature: {probe_temperature:.2f}°C")

        pub_sensor_data(client,topic, latest_data)
        
    time.sleep(1)  # Wait for 15 seconds
    #publish_random_number(client, "encyclopedia/temperature")  # Publish the random number



