import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('traffic_data.db')
df = pd.read_sql_query("SELECT * FROM CombinedData", conn)
conn.close()

if df.empty:
    print("No data to visualize.")
    exit()

# Convert timestamp to datetime for better visualizations
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Plot traffic speed over time
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['currentSpeed'], label='Current Speed', marker='o', color='blue')
plt.plot(df['timestamp'], df['freeFlowSpeed'], label='Free Flow Speed', marker='x', color='green')
plt.xlabel('Timestamp')
plt.ylabel('Speed (mph)')
plt.title('Traffic Speed Trends Over Time')
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Visualize ride demand over time
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['ride_demand'], label='Ride Demand', color='orange')
plt.xlabel('Timestamp')
plt.ylabel('Ride Demand')
plt.title('Ride Demand Trends Over Time')
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Correlation heatmap
plt.figure(figsize=(8, 6))
correlation = df[['currentSpeed', 'freeFlowSpeed', 'confidence', 'temperature', 'peakHour', 'ride_demand']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.show()
