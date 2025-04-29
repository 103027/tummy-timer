# models.py

from db import mongo

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
    Fetch the latest sensor reading from MongoDB.
    """
    latest = mongo.db.sensor_data.find().sort('timestamp', -1).limit(1)
    for doc in latest:
        return {
            "pet_present": doc.get("pet_present"),
            "weight": doc.get("weight"),
            "timestamp": doc.get("timestamp")
        }
    return None

def get_feeding_history():
    """
    Fetch feeding history - all sensor data sorted by time descending.
    (Optional if you want full table in frontend)
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
