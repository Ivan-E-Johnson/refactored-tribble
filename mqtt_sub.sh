#!/bin/bash

# MQTT broker settings
MQTT_BROKER="localhost"  # Change to the IP or hostname of your MQTT broker
MQTT_TOPIC="sensor/dht22"  # Change to the desired MQTT topic

# Subscribe to the MQTT topic
mosquitto_sub -h "$MQTT_BROKER" -t "$MQTT_TOPIC" -v

