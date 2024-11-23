import sqlite3
import pandas as pd

conn = sqlite3.connect('traffic_data.db')
df = pd.read_sql_query("SELECT * FROM CombinedData", conn)
conn.close()

if df.empty:
    print("The CombinedData table is empty.")
else:
    print(f"Data in CombinedData: {len(df)} rows")
    print(df.head())
