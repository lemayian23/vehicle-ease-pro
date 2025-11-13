from flask import Flask, jsonify
import threading
import websockets
import json
import asyncio
import time
from datetime import datetime

app = Flask(__name__)

# Store latest car data with fuel calculations
latest_data = {
    "rpm": 0,
    "coolant": 0, 
    "throttle": 0,
    "speed": 0,
    "gear": "N",
    "fuel_rate": 0.0,
    "trip_fuel": 0.0,
    "fuel_efficiency": 0.0,
    "trip_cost": 0.0
}

# Fuel calculation constants
FUEL_PRICE = 1.50  # $ per liter - adjust for your region
TRIP_START_TIME = time.time()
TRIP_DISTANCE = 0.0  # km

def calculate_gear(rpm, speed):
    """Calculate gear based on RPM and speed"""
    if speed == 0 or rpm < 500:
        return "N"
    
    # Simple gear calculation
    ratio = rpm / max(1, speed)
    
    if ratio > 300: return "1"
    elif ratio > 200: return "2" 
    elif ratio > 150: return "3"
    elif ratio > 120: return "4"
    elif ratio > 100: return "5"
    else: return "6"

def calculate_fuel_data(data):
    """Calculate real-time fuel consumption and efficiency"""
    global TRIP_DISTANCE
    
    # Base fuel consumption model (liters per hour)
    # Idle consumption + RPM factor + Throttle factor
    idle_consumption = 0.8  # liters/hour at idle
    rpm_factor = (data['rpm'] / 1000) * 0.5  # scales with RPM
    throttle_factor = (data['throttle'] / 100) * 1.2  # scales with throttle
    
    # Current fuel consumption rate (liters/hour)
    current_fuel_rate = idle_consumption + rpm_factor + throttle_factor
    
    # Convert to liters per second for trip calculation
    fuel_per_second = current_fuel_rate / 3600
    
    # Update trip distance (speed in km/h -> km per second)
    distance_per_second = data['speed'] / 3600
    TRIP_DISTANCE += distance_per_second
    
    # Calculate instant fuel efficiency (km/liter)
    instant_efficiency = 0.0
    if current_fuel_rate > 0 and data['speed'] > 0:
        instant_efficiency = data['speed'] / current_fuel_rate  # km/l
    
    # Update trip fuel consumption
    latest_data['fuel_rate'] = round(current_fuel_rate, 2)
    latest_data['trip_fuel'] += fuel_per_second
    latest_data['fuel_efficiency'] = round(instant_efficiency, 1)
    latest_data['trip_cost'] = round(latest_data['trip_fuel'] * FUEL_PRICE, 2)
    
    return latest_data

@app.route('/data')
def get_data():
    return jsonify(latest_data)

@app.route('/trip/reset', methods=['POST'])
def reset_trip():
    """Reset trip data"""
    global TRIP_START_TIME, TRIP_DISTANCE
    TRIP_START_TIME = time.time()
    TRIP_DISTANCE = 0.0
    latest_data['trip_fuel'] = 0.0
    latest_data['trip_cost'] = 0.0
    return jsonify({"status": "Trip reset"})

async def websocket_client():
    """Connect to OBD server and forward data"""
    uri = "ws://localhost:8765"
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to OBD server")
                while True:
                    data = await websocket.recv()
                    global latest_data
                    latest_data.update(json.loads(data))
                    
                    # Add gear calculation
                    latest_data['gear'] = calculate_gear(
                        latest_data.get('rpm', 0), 
                        latest_data.get('speed', 0)
                    )
                    
                    # Calculate fuel data
                    calculate_fuel_data(latest_data)
                    
        except Exception as e:
            print(f"WebSocket error: {e}")
            await asyncio.sleep(2)

def run_websocket_client():
    asyncio.new_event_loop().run_until_complete(websocket_client())

if __name__ == "__main__":
    # Start WebSocket client in background thread
    ws_thread = threading.Thread(target=run_websocket_client, daemon=True)
    ws_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=8766, debug=False)