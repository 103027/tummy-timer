from prophet import Prophet
from db import mongo
from flask import jsonify
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def predict_next_feeding():
    # Fetch historical data
    records = list(mongo.db.sensor_data.find().sort("timestamp", 1))
    
    if not records:
        return jsonify({"error": "No sensor data available"}), 400
    
    # Create a DataFrame with timestamps and food consumption amounts
    data = []
    for doc in records:
        try:
            timestamp = datetime.strptime(doc["timestamp"], "%Y-%m-%d %H:%M:%S")
            weight_change = doc.get("weight", 0)
            
            # Only consider positive weight changes as feeding events
            if weight_change > 0:
                data.append({
                    "ds": timestamp,
                    "y": weight_change  # Use actual weight change as value
                })
        except (ValueError, KeyError) as e:
            # Skip records with invalid timestamp format
            continue
    
    if len(data) < 5:
        return jsonify({"error": "Not enough feeding data to make prediction (minimum 5 events)"}), 400

    df = pd.DataFrame(data)
    
    # Add day of week and hour features to improve prediction
    df["day_of_week"] = df["ds"].dt.dayofweek
    df["hour"] = df["ds"].dt.hour
    
    # Train the model with additional seasonality
    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
        changepoint_prior_scale=0.05  # Balance flexibility and overfitting
    )
    
    # Add time-based features
    model.add_seasonality(name='hourly', period=24, fourier_order=5)
    model.fit(df)

    # Predict for the next 6 days hourly
    future = model.make_future_dataframe(periods=6*24, freq='h')
    forecast = model.predict(future)
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    
    # We'll store predictions for 5 days
    result = []
    
    # Process each of the next 5 days
    for day_offset in range(5):
        target_date = tomorrow + timedelta(days=day_offset)
        
        # Filter predictions for this day
        day_forecast = forecast[forecast["ds"].dt.date == target_date]
        
        # Get the average yhat value for this day to use in normalization
        day_avg = day_forecast["yhat"].mean()
        day_max = day_forecast["yhat"].max()
        
        if day_forecast.empty:
            continue
        
        # Find peaks where the predicted value is significantly above zero
        # and higher than neighboring hours
        potential_times = []
        
        for i in range(1, len(day_forecast) - 1):
            current = day_forecast.iloc[i]
            prev_hour = day_forecast.iloc[i-1]
            next_hour = day_forecast.iloc[i+1]
            
            # Check if this is a local maximum and above threshold
            if (current["yhat"] > 0.1 and 
                current["yhat"] > prev_hour["yhat"] and 
                current["yhat"] > next_hour["yhat"]):
                
                # New confidence calculation based on normalized prediction value
                # Scale from 40-90% to avoid extreme values
                normalized_value = current["yhat"] / (df["y"].max() * 0.5)  # Normalize against half the max value
                confidence = max(40, min(90, int(40 + normalized_value * 50)))  # Scale to 40-90% range
                
                potential_times.append({
                    "time": current["ds"],
                    "yhat": current["yhat"],
                    "confidence": confidence
                })
        
        # Sort by predicted value and take top 3
        potential_times.sort(key=lambda x: x["yhat"], reverse=True)
        top_times = potential_times[:3]
        
        # If every day should have at least one prediction with moderate confidence
        if not potential_times or all(t["confidence"] < 50 for t in potential_times):
            best_hour = day_forecast.loc[day_forecast["yhat"].idxmax()]
            normalized_value = best_hour["yhat"] / (df["y"].max() * 0.5)
            confidence = max(45, min(90, int(40 + normalized_value * 50)))
            
            # Check if this time is already in top_times
            best_time = best_hour["ds"]
            if not any(t["time"] == best_time for t in top_times):
                top_times.append({
                    "time": best_time,
                    "yhat": best_hour["yhat"],
                    "confidence": confidence
                })
        
        # If we don't have enough peaks, add the highest values from the day
        if len(top_times) < 3:
            remaining_needed = 3 - len(top_times)
            # Get times we haven't already included
            existing_times = {t["time"] for t in top_times}
            additional_times = day_forecast[~day_forecast["ds"].isin(existing_times)]
            
            if not additional_times.empty:
                additional_times = additional_times.nlargest(remaining_needed, "yhat")
                
                for _, row in additional_times.iterrows():
                    normalized_value = row["yhat"] / (df["y"].max() * 0.5)
                    confidence = max(40, min(90, int(40 + normalized_value * 50)))
                    
                    top_times.append({
                        "time": row["ds"],
                        "yhat": row["yhat"],
                        "confidence": confidence
                    })
        
        # Add to results
        for entry in top_times:
            result.append({
                "predicted_time": entry["time"].strftime("%Y-%m-%d %H:%M:%S"),
                "confidence": entry["confidence"],
                "day": entry["time"].strftime("%A")  # Add day of week for better readability
            })
    
    # Add additional checks to ensure all confidence values are within proper range
    for entry in result:
        if not 0 <= entry["confidence"] <= 100:
            entry["confidence"] = max(40, min(90, entry["confidence"]))
    
    # Sort by date and time for better readability
    result.sort(key=lambda x: x["predicted_time"])
    
    return jsonify(result)