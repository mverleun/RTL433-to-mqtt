#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import subprocess
import sys
import time
import paho.mqtt.client as mqtt
import os
import json

# Config section
# Uncomment these lines if your MQTT server requires authentication
#MQTT_USER="mqtt-user"
#MQTT_PASS="mqtt-password"
MQTT_HOST="mqtt.example.com"
MQTT_PORT=1883
MQTT_TOPIC="sensors/rtl_433"
MQTT_QOS=0
# End config section

rtl_433_cmd = "/usr/local/bin/rtl_433 -G -F json" # linux

# Define MQTT event callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

# Setup MQTT connection

mqttc = mqtt.Client()
# Assign event callbacks
#mqttc.on_message = on_message
mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Uncomment the next line if your MQTT server requires authentication
#mqttc.username_pw_set(MQTT_USER, password=MQTT_PASS)
mqttc.connect(MQTT_HOST, MQTT_PORT, 60)

mqttc.loop_start()

# Start RTL433 listener
rtl433_proc = subprocess.Popen(rtl_433_cmd.split(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)


while True:
    for line in iter(rtl433_proc.stdout.readline, '\n'):
        if "time" in line:
            mqttc.publish(MQTT_TOPIC, payload=line,qos=MQTT_QOS)
            json_dict = json.loads(line)
            for item in json_dict:
                value = json_dict[item]
                if "model" in item:
                    subtopic=value

            for item in json_dict:
                value = json_dict[item]
                if not "model" in item:
                    mqttc.publish(MQTT_TOPIC+"/"+subtopic+"/"+item, payload=value,qos=MQTT_QOS)
