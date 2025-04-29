from flask import Flask, jsonify
from flask_cors import CORS
from db import init_db
from models import get_latest_data
import mqtt_client
import prediction

app = Flask(__name__)
CORS(app)

init_db(app)
mqtt_client.mqtt_init()

@app.route("/")
def index():
    return jsonify({"message": "TummyTimer Flask Backend is running"})

@app.route("/sensor/latest", methods=["GET"])
def latest_sensor():
    data = get_latest_data()
    return jsonify(data) if data else jsonify({"message": "No data yet"}), 404

@app.route("/predict/next-feeding", methods=["GET"])
def predict():
    return prediction.predict_next_feeding()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
