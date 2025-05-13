import paho.mqtt.client as mqtt
import json
import ssl
from datetime import datetime
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
        from models import save_sensor_data
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
    try:
        existing_schedules = list(mongo.db.schedules.find({}, {'_id': 0}))
        
        if isinstance(new_schedule, str):
            try:
                new_schedule = json.loads(new_schedule)
            except json.JSONDecodeError:
                print("Error parsing JSON schedule data")
                return
        
        existing_schedules.append(new_schedule)
        schedules_json = json.dumps(existing_schedules)
        client.publish("petfeeder/schedule", schedules_json)
        print(f"Published updated schedule array to MQTT with {len(existing_schedules)} schedules")
            
        
    except Exception as e:
        print(f"Error publishing schedule array: {str(e)}")


def publish_schedule_array(schedules_array):
    try:
        clean_schedules = []
        for schedule in schedules_array:
            clean_schedule = {k: v for k, v in schedule.items() if k != '_id'}
            clean_schedules.append(clean_schedule)
            
        schedules_json = json.dumps(clean_schedules)
        client.publish("petfeeder/schedule", schedules_json)
        print(f"Published updated schedule array to MQTT with {len(clean_schedules)} schedules")
    except Exception as e:
        print(f"Error publishing schedule array: {str(e)}")

def publish_updated_schedule(updated_schedule):
    try:
        if not updated_schedule.get('_id'):
            print("Error: No _id provided in the updated schedule")
            return False
            
        schedule_id = updated_schedule.pop('_id')
        try:
            schedule_id = ObjectId(schedule_id)
        except:
            print("Error: Invalid _id format")
            return False
            
        result = mongo.db.schedules.update_one(
            {"_id": schedule_id},
            {"$set": updated_schedule}
        )
        
        if result.matched_count == 0:
            print(f"No schedule found with _id: {schedule_id}")
            return False
            
        all_schedules = list(mongo.db.schedules.find({}, {'_id': 0}))
        
        schedules_json = json.dumps(all_schedules)
        client.publish("petfeeder/schedule", schedules_json)
        print(f"Published updated schedule array to MQTT with {len(all_schedules)} schedules")
        return True
        
    except Exception as e:
        print(f"Error publishing updated schedule: {str(e)}")
        return False

def mqtt_init():
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_start()
