# models.py

from db import mongo
from schedule_manager import get_schedule
from mqtt_client import publish_updated_schedule
from datetime import datetime, timedelta


def was_fed_today():
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_feed = mongo.db.sensor_data.find_one({
        "timestamp": {"$regex": f"^{today_str}"}
    })

    return {
        "fed_today": today_feed is not None
    }


def save_sensor_data(data):
    mongo.db.sensor_data.insert_one(data)
    data_ = get_latest_data()
    # print(data_)

def get_latest_data():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_str = today.strftime("%Y-%m-%d")

    total_weight_today = 0
    data_list = []

    # Check if the Schedule is completed or not

    cursor = mongo.db.sensor_data.find().sort("timestamp", -1)  # All sensor data sorted by time
    sensor_timestamp = datetime.strptime(cursor[0]["timestamp"], "%Y-%m-%d %H:%M:%S")
    # print(sensor_timestamp)

    today = datetime.now().date()
    sensor_date = sensor_timestamp.date()
    sensor_time = sensor_timestamp.time()

    schedules = get_schedule()
    print("Before Updated Schedule",schedules)

    for schedule in schedules:
        start = datetime.strptime(schedule["startTime"], "%H:%M").time()
        end = datetime.strptime(schedule["endTime"], "%H:%M").time()
        
        if sensor_date == today and start <= sensor_time <= end:
            today_day_name = today.strftime("%a")
            if today_day_name in schedule["days"]:
                schedule["flag"] = True
            publish_updated_schedule(schedule)

    print("updated schedules",schedules)

    # Finding Todays Bowl Status
    
    for doc in cursor:
        timestamp_str = doc.get("timestamp")
        
        data_item = {
            "pet_present": doc.get("pet_present"),
            "food_dispensed": doc.get("food_dispensed"),
            "weight": doc.get("weight"),
            "timestamp": timestamp_str
        }
        data_list.append(data_item)
        
        if timestamp_str and timestamp_str.startswith(today_str):
            weight = doc.get("weight", 0)
            if weight and doc.get("food_dispensed") == True:
                total_weight_today += weight
    
    return {
        "total_weight_today": total_weight_today,
        "data": data_list
    }


def get_feeding_history():
    history = mongo.db.sensor_data.find().sort('timestamp', -1)
    return [
        {
            "pet_present": doc.get("pet_present"),
            "weight": doc.get("weight"),
            "timestamp": doc.get("timestamp")
        }
        for doc in history
    ]

def reset_feeding_flags():
    today = datetime.now().date()
    schedules = mongo.db.schedules.find({"days": today.strftime("%a")})
    
    for schedule in schedules:
        feeding_time = datetime.strptime(schedule["endTime"], "%H:%M").time()
        current_time = datetime.now().time()
        
        if current_time > feeding_time:
            mongo.db.schedules.update_one(
                {"_id": schedule["_id"]},
                {"$set": {"flag": False}}
            )
            print(f"Flag reset for schedule: {schedule['startTime']} - {schedule['endTime']}")