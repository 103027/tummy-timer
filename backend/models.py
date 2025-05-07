# models.py

from db import mongo
from schedule_manager import get_schedule
from mqtt_client import publish_updated_schedule
from datetime import datetime, timedelta


def was_fed_today():
    """
    Check if any feeding happened today by looking at today’s date in timestamps.
    """
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_feed = mongo.db.sensor_data.find_one({
        "timestamp": {"$regex": f"^{today_str}"}
    })

    return {
        "fed_today": today_feed is not None
    }


def save_sensor_data(data):
    """
    Save incoming sensor data to MongoDB.
    Expected data format:
    {
        "pet_present": true,
        "weight": 150,
        "timestamp": "2025-04-29 20:30:00"
    }
    """
    mongo.db.sensor_data.insert_one(data)

def get_latest_data():
    """
    Fetch sensor readings from MongoDB and calculate total weight for today.
    
    Returns:
        dict: Dictionary containing total weight for today and all sensor readings
    """
    # Get today's date (start of day)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    # Format dates as strings to match your timestamp format
    today_str = today.strftime("%Y-%m-%d")
    
    # Calculate total weight for today
    total_weight_today = 0
    
    # Get all sensor data sorted by timestamp
    data_list = []
    cursor = mongo.db.sensor_data.find().sort("timestamp", -1)


    sensor_timestamp = datetime.strptime(cursor[0]["timestamp"], "%Y-%m-%d %H:%M:%S")

    # Get today's date
    today = datetime.now().date()
    sensor_date = sensor_timestamp.date()
    sensor_time = sensor_timestamp.time()

    schedules = get_schedule()
    print("first",schedules)

    for schedule in schedules:
        start = datetime.strptime(schedule["startTime"], "%H:%M").time()
        end = datetime.strptime(schedule["endTime"], "%H:%M").time()
        
        if sensor_date == today and start <= sensor_time <= end:
            # Check if today’s day name is in schedule days
            today_day_name = today.strftime("%a")  # e.g., 'Wed'
            if today_day_name in schedule["days"]:
                schedule["flag"] = True
            publish_updated_schedule(schedule)

    print(schedules)
    
    for doc in cursor:
        timestamp_str = doc.get("timestamp")
        
        # Add document to full data list
        data_item = {
            "pet_present": doc.get("pet_present"),
            "food_dispensed": doc.get("food_dispensed"),
            "weight": doc.get("weight"),
            "timestamp": timestamp_str
        }
        data_list.append(data_item)
        
        # Check if the document is from today
        if timestamp_str and timestamp_str.startswith(today_str):
            weight = doc.get("weight", 0)
            if weight and doc.get("food_dispensed") == True:
                total_weight_today += weight
    
    return {
        "total_weight_today": total_weight_today,
        "data": data_list
    }


def get_feeding_history():
    """
    Fetch feeding history - all sensor data sorted by time descending.
    """
    history = mongo.db.sensor_data.find().sort('timestamp', -1)
    return [
        {
            "pet_present": doc.get("pet_present"),
            "weight": doc.get("weight"),
            "timestamp": doc.get("timestamp")
        }
        for doc in history
    ]
