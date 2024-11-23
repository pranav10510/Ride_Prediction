import sqlite3
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('ride_demand_model.pkl')

# Fetch the latest data from CombinedData
conn = sqlite3.connect('traffic_data.db')
latest_data = pd.read_sql_query("SELECT * FROM CombinedData ORDER BY timestamp DESC LIMIT 1", conn)
conn.close()

# Prepare features for prediction
latest_data['eventCount'] = latest_data['eventCount'].fillna(0)  # Handle missing values
features = latest_data[['currentSpeed', 'freeFlowSpeed', 'confidence', 'temperature', 'eventCount']].values
prediction = model.predict(features)

print("Predicted Ride Demand:", prediction[0])