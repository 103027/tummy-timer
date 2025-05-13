from flask import Flask, jsonify, request
from flask_cors import CORS
from db import init_db
from models import get_latest_data
import mqtt_client
import prediction
import schedule_manager
from models import was_fed_today
from models import get_feeding_history, reset_feeding_flags
from schedule_manager import get_schedule, save_schedule
import json
from db import mongo
from bson.objectid import ObjectId
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
CORS(app)

init_db(app)
mqtt_client.mqtt_init()

@app.route("/")
def index():
    return jsonify({"message": "TummyTimer Flask Backend is running"})

@app.route("/sensor/portions", methods=["GET"])
def latest_sensor():
    data = get_latest_data()
    return jsonify(data) if data else jsonify({"message": "No data yet"}), 200

@app.route("/status/today", methods=["GET"])
def is_fed_today():
    status = was_fed_today()
    return jsonify(status)

@app.route("/control/feed-now", methods=["POST"])
def feed_now():
    mqtt_client.publish_feed_now()
    return jsonify({"message": "Feed command sent"})

@app.route("/history", methods=["GET"])
def history():
    return jsonify(get_feeding_history())

@app.route("/schedule", methods=["GET", "POST"])
def manage_schedule():
    if request.method == "GET":
        schedule = get_schedule()
        return jsonify(schedule)
    
    if request.method == "POST":
        raw_data = request.get_data(as_text=True)
        if not raw_data:
            return jsonify({"error": "No data received"}), 400

        print("Received raw schedule JSON:", raw_data)
        
        try:
            data = json.loads(raw_data)
            existing_schedules = list(mongo.db.schedules.find({}, {'_id': 0}))
            is_duplicate = False
            for schedule in existing_schedules:
                if (schedule.get('startTime') == data.get('startTime') and schedule.get('endTime') == data.get('endTime')):
                    is_duplicate = True
                    break
        
            if is_duplicate:
                return jsonify({"message": "Duplicate Schedule"})
            else:
                save_schedule(data)
                mqtt_client.publish_schedule(raw_data)
                return jsonify({"message": "Schedule saved and published to Pi"})
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON format"}), 400


@app.route("/predict/next-feeding", methods=["GET"])
def predict():
    return prediction.predict_next_feeding()

@app.route("/schedule/", methods=["DELETE"])
def delete_schedule():
    try:
        data = request.get_json()
        index = data.get("index")
        
        all_schedules = list(mongo.db.schedules.find())
        
        if index is None or index < 0 or index >= len(all_schedules):
            return jsonify({"error": "Invalid index"}), 400
        
        object_id = all_schedules[index]["_id"]
        
        result = mongo.db.schedules.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            return jsonify({"error": "Schedule not found"}), 404

        remaining_schedules = list(mongo.db.schedules.find({}, {'_id': 0}))
        mqtt_client.publish_schedule_array(remaining_schedules)
        return jsonify({"message": "Schedule deleted", "remainingSchedules": remaining_schedules})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


scheduler = BackgroundScheduler()
scheduler.add_job(reset_feeding_flags, 'interval', hours=24)  # Run every 24 hours
scheduler.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
