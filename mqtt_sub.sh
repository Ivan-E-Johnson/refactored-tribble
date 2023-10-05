#!/bin/bash

# MQTT broker settings
MQTT_BROKER="localhost"  # Change to the IP or hostname of your MQTT broker
MQTT_TOPIC="sensors/data/human_readable"

mosquitto_sub -h "$MQTT_BROKER" -t "$MQTT_TOPIC" -v

