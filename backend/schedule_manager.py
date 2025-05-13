from flask import current_app
from pymongo import DESCENDING
from db import mongo
from bson.objectid import ObjectId

def get_schedule():
    schedules_list = []
    cursor = mongo.db.schedules.find().sort("_id", DESCENDING)
    
    for schedule in cursor:
        schedule["_id"] = str(schedule["_id"])
        schedules_list.append(schedule)
    
    return schedules_list

def save_schedule(data):
    mongo.db.schedules.insert_one(data)

def update_schedule(data):
    try:
        # Extract the _id field before updating
        schedule_id = data.pop("_id", None)
        
        if not schedule_id:
            return {"success": False, "error": "No _id provided"}
            
        # Validate ObjectId format
        try:
            object_id = ObjectId(schedule_id)
        except:
            return {"success": False, "error": "Invalid _id format"}
        
        result = mongo.db.schedules.update_one(
            {"_id": object_id},
            {"$set": data}
        )
        
        if result.matched_count > 0:
            return {"success": True, "modified_count": result.modified_count}
        else:
            return {"success": False, "error": "No document found with that _id"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}
