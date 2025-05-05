import paho.mqtt.client as mqtt
import json
import ssl
from datetime import datetime
from models import save_sensor_data
from bson.objectid import ObjectId
from db import mongo

BROKER = "493700728f8244298020d35f5eeadd2e.s1.eu.hivemq.cloud"
PORT = 8883
TOPIC = "petfeeder/sensor"
USERNAME = "hassan"
PASSWORD = "IOTproject10"


client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to HiveMQ Cloud MQTT Broker")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("Received MQTT Message:", payload)
        save_sensor_data(payload)
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

def publish_feed_now():
    payload = {
        "action": "dispense",
        "portion": 1,
    }
    client.publish("petfeeder/control", json.dumps(payload))
    print("Feed-now command published")

def publish_schedule(new_schedule):
    """
    Publish an array of schedules to MQTT, adding the new schedule to existing ones.
    
    Args:
        new_schedule: The new schedule data to add
    """
    try:
        # Get the current schedule array from the database
        existing_schedules = list(mongo.db.schedules.find({}, {'_id': 0}))  # Exclude _id fields
        
        # If new_schedule is a string (raw JSON), parse it
        if isinstance(new_schedule, str):
            try:
                new_schedule = json.loads(new_schedule)
            except json.JSONDecodeError:
                print("Error parsing JSON schedule data")
                return
        
        # Check if this is a duplicate schedule
        is_duplicate = False
        for schedule in existing_schedules:
            if (schedule.get('startTime') == new_schedule.get('startTime') and 
                schedule.get('endTime') == new_schedule.get('endTime')):
                is_duplicate = True
                break
        
        # Only add if it's not a duplicate
        if not is_duplicate:
            existing_schedules.append(new_schedule)
        
        # Convert the entire array to JSON and publish
        schedules_json = json.dumps(existing_schedules)
        client.publish("petfeeder/schedule", schedules_json)
        print(f"Published updated schedule array to MQTT with {len(existing_schedules)} schedules")
    except Exception as e:
        print(f"Error publishing schedule array: {str(e)}")


def publish_schedule_array(schedules_array):
    """
    Publish an array of schedules to MQTT.
    
    Args:
        schedules_array: List of schedule objects
    """
    try:
        # Remove any ObjectId that might be present
        clean_schedules = []
        for schedule in schedules_array:
            clean_schedule = {k: v for k, v in schedule.items() if k != '_id'}
            clean_schedules.append(clean_schedule)
            
        # Convert to JSON and publish
        schedules_json = json.dumps(clean_schedules)
        client.publish("petfeeder/schedule", schedules_json)
        print(f"Published updated schedule array to MQTT with {len(clean_schedules)} schedules")
    except Exception as e:
        print(f"Error publishing schedule array: {str(e)}")

def mqtt_init():
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()
