"""
================================================================================
ORBITLINK - REAL-TIME LIVE SATELLITE SIGNAL LOSS PREDICTION
Fetches LIVE Meteorological Telemetry from Open-Meteo API
Feeds Real Weather Data directly into our Trained Random Forest Model
Author: Roshni Priyadarshini Behera (USN: 25MSFDR009)
Guide : DR. M N NACHAPPA
================================================================================
"""

import os
import json
import urllib.request
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 1. Train the Production Random Forest Model
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "dataset", "satellite_atmospheric_attenuation.csv")
if not os.path.exists(csv_path):
    csv_path = os.path.join(base_dir, "..", "analytics", "dataset", "satellite_atmospheric_attenuation.csv")

df = pd.read_csv(csv_path)
features = ['elevation_angle_deg', 'frequency_ghz', 'rain_rate_mm_hr',
            'cloud_liquid_water_g_m3', 'surface_temp_c', 'relative_humidity_pct']
X = df[features]
y = df['signal_attenuation_db']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
rf = RandomForestRegressor(n_estimators=100, max_depth=14, random_state=42)
rf.fit(X_train, y_train)

print("\n" + "=" * 78)
print("   ORBITLINK: REAL-TIME SATELLITE SIGNAL ATTENUATION PREDICTION")
print("   Grounded in Live Atmospheric Weather Streams via Open-Meteo API")
print("   Student: Roshni Priyadarshini Behera (USN: 25MSFDR009)")
print("   Subject: Statistics & Data Analytics | Guide: DR. M N NACHAPPA")
print("=" * 78)

# 2. Real Himalayan Mountain Coordinates
mountain_targets = [
    {
        "name": "Hampta Pass (Himachal Pradesh)",
        "lat": 32.24,
        "lng": 77.36,
        "elevation_m": 4287,
        "look_angle": 48.5,
        "band": "Ku-band (14.2 GHz)"
    },
    {
        "name": "Pin Parvati Pass (Himachal Pradesh)",
        "lat": 31.85,
        "lng": 77.80,
        "elevation_m": 5319,
        "look_angle": 35.0,
        "band": "Ka-band (26.5 GHz)"
    },
    {
        "name": "Kedarkantha (Uttarakhand)",
        "lat": 31.02,
        "lng": 78.17,
        "elevation_m": 3810,
        "look_angle": 62.0,
        "band": "Ku-band (14.2 GHz)"
    },
    {
        "name": "Roopkund Mystery Lake (Uttarakhand)",
        "lat": 30.26,
        "lng": 79.73,
        "elevation_m": 5029,
        "look_angle": 28.0,
        "band": "Ka-band (26.5 GHz)"
    }
]

print("\n[+] FETCHING LIVE SATELLITE & ATMOSPHERIC TELEMETRY FROM WEATHER API...\n")

for m in mountain_targets:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={m['lat']}&longitude={m['lng']}&current=temperature_2m,relative_humidity_2m,precipitation,rain,cloud_cover"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'OrbitLink/1.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            curr = data.get('current', {})
            
            temp_c = curr.get('temperature_2m', 15.0)
            humidity_pct = curr.get('relative_humidity_2m', 50.0)
            rain_mm = curr.get('rain', 0.0)
            cloud_cover_pct = curr.get('cloud_cover', 20.0)
            cloud_water_est = round((cloud_cover_pct / 100.0) * 0.8, 3)
            
            freq_val = 26.5 if "26.5" in m['band'] else 14.2
            
            live_input = pd.DataFrame([{
                'elevation_angle_deg': m['look_angle'],
                'frequency_ghz': freq_val,
                'rain_rate_mm_hr': rain_mm,
                'cloud_liquid_water_g_m3': cloud_water_est,
                'surface_temp_c': temp_c,
                'relative_humidity_pct': humidity_pct
            }])
            
            predicted_loss_db = rf.predict(live_input)[0]
            
            if predicted_loss_db < 2.0:
                health = "EXCELLENT (100% Data Downlink Rate)"
                status_symbol = "🟢"
            elif predicted_loss_db < 6.0:
                health = "MODERATE ATTENUATION (80% Rate Adaptive Downlink)"
                status_symbol = "🟡"
            elif predicted_loss_db < 12.0:
                health = "SEVERE RAIN FADE (60% Downlink Rate - Triage Orders)"
                status_symbol = "🟠"
            else:
                health = "CRITICAL STORM FADE (35% Emergency Only)"
                status_symbol = "🔴"

            print(f"📍 Location: {m['name']} (Altitude: {m['elevation_m']} m)")
            print(f"   Coordinates  : {m['lat']}° N, {m['lng']}° E | Link Band: {m['band']}")
            print(f"   LIVE Weather : Temp = {temp_c}°C | Rain = {rain_mm} mm/hr | Humidity = {humidity_pct}% | Cloud = {cloud_cover_pct}%")
            print(f"   Look Angle   : {m['look_angle']}° Elevation")
            print(f"   ML Prediction: {status_symbol} Predicted Signal Attenuation = {predicted_loss_db:.2f} dB")
            print(f"   Channel State: {health}\n")

    except Exception as e:
        print(f"[!] Could not connect to live weather API for {m['name']}: {e}\n")

print("=" * 78)
print("  [✓] LIVE TELEMETRY INGESTION & ML INFERENCE COMPLETED SUCCESSFULLY!")
print("==============================================================================\n")

