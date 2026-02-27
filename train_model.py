import sqlite3
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

# Connect DB
conn = sqlite3.connect("instance/smartoutfit.db")

# Load tables
history = pd.read_sql_query("SELECT * FROM outfit_history", conn)
clothing = pd.read_sql_query("SELECT * FROM clothing_item", conn)

conn.close()

# If no history, stop
if history.empty:
    print("No outfit history found.")
    exit()

# Prepare dataset
rows = []

for _, row in history.iterrows():
    item_ids = list(map(int, row["items_used"].split(",")))

    items = clothing[clothing["id"].isin(item_ids)]

    if items.empty:
        continue

    favorite_count = items["favorited"].sum()
    avg_times_worn = items["times_worn"].mean()
    unique_categories = items["category"].nunique()
    total_items = len(items)

    # Target (implicit feedback)
    target = 1 if avg_times_worn >= 1 else 0

    rows.append({
        "event": row["event"],
        "weather": row["weather"],
        "favorite_count": favorite_count,
        "avg_times_worn": avg_times_worn,
        "unique_categories": unique_categories,
        "total_items": total_items,
        "target": target
    })

df = pd.DataFrame(rows)

if df.empty:
    print("No valid training data.")
    exit()

# Encode categorical features
le_event = LabelEncoder()
le_weather = LabelEncoder()

df["event_encoded"] = le_event.fit_transform(df["event"])
df["weather_encoded"] = le_weather.fit_transform(df["weather"])

X = df[[
    "event_encoded",
    "weather_encoded",
    "favorite_count",
    "avg_times_worn",
    "unique_categories",
    "total_items"
]]

y = df["target"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model & encoders
joblib.dump(model, "ml_model.pkl")
joblib.dump(le_event, "event_encoder.pkl")
joblib.dump(le_weather, "weather_encoder.pkl")

print("Model trained and saved successfully.")