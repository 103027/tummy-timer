from flask import Flask, jsonify, request
from flask_cors import CORS
from db import init_db
from models import get_latest_data
import mqtt_client
import prediction
import schedule_manager
from models import was_fed_today
from models import get_feeding_history
from schedule_manager import get_schedule, save_schedule
import json
from db import mongo
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

init_db(app)
mqtt_client.mqtt_init()

@app.route("/")
def index():
    return jsonify({"message": "TummyTimer Flask Backend is running"})

# 1. Get latest sensor data (already present)
@app.route("/sensor/portions", methods=["GET"])
def latest_sensor():
    data = get_latest_data()
    return jsonify(data) if data else jsonify({"message": "No data yet"}), 200

# 2. Is pet fed today?
@app.route("/status/today", methods=["GET"])
def is_fed_today():
    status = was_fed_today()
    return jsonify(status)

# 4. Feed now (manual control)
@app.route("/control/feed-now", methods=["POST"])
def feed_now():
    mqtt_client.publish_feed_now()
    return jsonify({"message": "Feed command sent"})

# 5. Get feeding history
@app.route("/history", methods=["GET"])
def history():
    return jsonify(get_feeding_history())

# 6. Schedule management
@app.route("/schedule", methods=["GET", "POST"])
def manage_schedule():
    if request.method == "GET":
        schedule = get_schedule()
        return jsonify(schedule)
    
    if request.method == "POST":
        # Get the raw JSON data as a string
        raw_data = request.get_data(as_text=True)
        if not raw_data:
            return jsonify({"error": "No data received"}), 400

        print("Received raw schedule JSON:", raw_data)
        
        # Parse the JSON for database storage
        try:
            data = json.loads(raw_data)
            save_schedule(data)
            
            # Keep raw JSON for MQTT
            mqtt_client.publish_schedule(raw_data)
            
            return jsonify({"message": "Schedule saved and published to Pi"})
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format"}), 400


# 7. Predict next feeding time (already present)
@app.route("/predict/next-feeding", methods=["GET"])
def predict():
    return prediction.predict_next_feeding()

@app.route("/schedule/", methods=["DELETE"])
def delete_schedule():
    try:
        data = request.get_json()
        index = data.get("index")
        
        # Get all schedules sorted by time (or however you want to maintain order)
        all_schedules = list(mongo.db.schedules.find())
        
        if index is None or index < 0 or index >= len(all_schedules):
            return jsonify({"error": "Invalid index"}), 400
        
        # Get the ObjectId of the schedule to delete
        object_id = all_schedules[index]["_id"]
        
        # Delete it
        result = mongo.db.schedules.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            return jsonify({"error": "Schedule not found"}), 404

        # Return updated list
        remaining_schedules = list(mongo.db.schedules.find({}, {'_id': 0}))

        # Optional: publish to MQTT
        mqtt_client.publish_schedule_array(remaining_schedules)

        return jsonify({"message": "Schedule deleted", "remainingSchedules": remaining_schedules})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
