import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

conn = sqlite3.connect('traffic_data.db')
df = pd.read_sql_query("SELECT * FROM CombinedData", conn)
conn.close()

if df.empty:
    raise ValueError("The CombinedData table is empty. Please fetch data first.")

df.fillna(0, inplace=True)
df['currentSpeed'] += np.random.uniform(-5, 5, size=len(df))
df['freeFlowSpeed'] += np.random.uniform(-5, 5, size=len(df))
df['confidence'] += np.random.uniform(-0.1, 0.1, size=len(df))
df['temperature'] += np.random.uniform(-2, 2, size=len(df))

df['ride_demand'] = (
    df['currentSpeed'] * 2 
    - df['confidence'] * 0.5 
    + df['temperature'] * 0.1 
    + df['peakHour'] * 5
)

X = df[['currentSpeed', 'freeFlowSpeed', 'confidence', 'temperature', 'peakHour']]
y = df['ride_demand']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))

import joblib
joblib.dump(model, 'ride_demand_model.pkl')
print("Model saved as 'ride_demand_model.pkl'.")
