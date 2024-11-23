import requests
import sqlite3
from datetime import datetime, timedelta
import time

# Your API keys
traffic_api_key = "tiJdaJNLyyGkx2LARkZ6qsd08Qg2GKZG"
weather_api_key = "e32d98164f138035a567a3b408742c21"

# API URLs
traffic_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
weather_url = "https://api.openweathermap.org/data/2.5/weather"

# API parameters
traffic_params = {"key": traffic_api_key, "point": "34.0522,-118.2437"}
weather_params = {"q": "Los Angeles,US", "appid": weather_api_key, "units": "imperial"}

def fetch_and_store_all_data():
    print("Fetching traffic data...")
    traffic_response = requests.get(traffic_url, params=traffic_params)
    if traffic_response.status_code == 200:
        traffic_data = traffic_response.json().get("flowSegmentData", {})
        current_speed = traffic_data.get("currentSpeed", None)
        free_flow_speed = traffic_data.get("freeFlowSpeed", None)
        confidence = traffic_data.get("confidence", None)
        print("Traffic data fetched successfully.")
    else:
        print(f"Traffic API Error: {traffic_response.status_code}")
        current_speed = free_flow_speed = confidence = None

    print("Fetching weather data...")
    weather_response = requests.get(weather_url, params=weather_params)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        print("Weather data fetched successfully.")
    else:
        print(f"Weather API Error: {weather_response.status_code}")
        temperature = None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('traffic_data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CombinedData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            currentSpeed REAL,
            freeFlowSpeed REAL,
            confidence REAL,
            temperature REAL,
            peakHour INTEGER
        )
    ''')

    # Determine if the current time is during peak hours
    current_hour = datetime.now().hour
    peak_hour = 1 if 7 <= current_hour <= 9 or 16 <= current_hour <= 19 else 0

    cursor.execute('''
        INSERT INTO CombinedData (timestamp, currentSpeed, freeFlowSpeed, confidence, temperature, peakHour)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, current_speed, free_flow_speed, confidence, temperature, peak_hour))
    conn.commit()
    conn.close()

    print(f"Data inserted into CombinedData at {timestamp}.")

# Fetch data every minute for 5 iterations (simulate multiple data points for testing)
for _ in range(5):
    fetch_and_store_all_data()
    time.sleep(60)  # Wait 60 seconds before fetching again
