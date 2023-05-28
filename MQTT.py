import json
import datetime
import os
import paho.mqtt.client as mqtt

LOG_FILE = 'mqtt_requests.json'

def create_log_file():
    with open(LOG_FILE, 'w') as file:
        pass  # Create an empty file

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect to MQTT broker. Error code:", rc)

    # Subscribe to all topics
    client.subscribe("#")

def on_message(client, userdata, msg):
    # Get current Unix timestamp
    timestamp = int(datetime.datetime.now().timestamp())

    payload = {
        'timestamp': timestamp,
        'topic': msg.topic,
        'message': msg.payload.decode('utf-8')
    }

    print(payload)
    
    # Write to the log file
    with open(LOG_FILE, 'a') as file:
        file.write(json.dumps(payload) + '\n')

    print("Received MQTT request and recorded it as JSON")

if not os.path.exists(LOG_FILE):
    create_log_file()
    print("Created log file:", LOG_FILE)

# Create an MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# MQTT broker
client.connect("localhost", 1883, 60)

client.loop_forever()