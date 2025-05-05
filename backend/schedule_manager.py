from flask import current_app
from pymongo import DESCENDING
from db import mongo

def get_schedule():
    """
    Retrieve all feeding schedules from the database.
    
    Returns:
        list: List of schedule documents with ObjectId converted to string
    """
    schedules_list = []
    cursor = mongo.db.schedules.find().sort("_id", DESCENDING)
    
    for schedule in cursor:
        # Convert ObjectId to string to make it JSON serializable
        schedule["_id"] = str(schedule["_id"])
        schedules_list.append(schedule)
    
    return schedules_list

def save_schedule(data):
    mongo.db.schedules.insert_one(data)
