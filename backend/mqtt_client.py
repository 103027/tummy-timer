# mqtt_client.py

import paho.mqtt.client as mqtt
import json
from models import save_sensor_data

BROKER = "localhost"
PORT = 1883
TOPIC = "petfeeder/sensor"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("Received MQTT Message:", payload)
        save_sensor_data(payload)
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

def mqtt_init():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()
