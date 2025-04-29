# prediction.py

from db import mongo
from prophet import Prophet
import pandas as pd

def train_model():
    # Fetch all feeding data
    sensor_data = list(mongo.db.sensor_data.find({"pet_present": True}))

    if len(sensor_data) < 10:
        return None  # Not enough data to train

    # Prepare DataFrame for Prophet
    df = pd.DataFrame(sensor_data)
    df['ds'] = pd.to_datetime(df['timestamp'])
    df['y'] = 1  # Each event where pet was present = 1 (binary feeding event)

    # Aggregate by hour
    df = df.resample('H', on='ds').sum().reset_index()

    model = Prophet()
    model.fit(df[['ds', 'y']])

    return model

def predict_next_feeding():
    model = train_model()

    if model is None:
        return {"message": "Not enough data to predict yet."}

    future = model.make_future_dataframe(periods=24, freq='H')
    forecast = model.predict(future)

    # Find next time where probability > 0.5
    future_feeds = forecast[forecast['yhat'] > 0.5]

    if not future_feeds.empty:
        next_feed_time = future_feeds.iloc[0]['ds']
        return {"next_feeding_time": str(next_feed_time)}
    else:
        return {"message": "No upcoming feeding time predicted."}
