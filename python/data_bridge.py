from flask import Flask, jsonify
import threading
import websockets
import json
import asyncio

app = Flask(__name__)

# Store latest car data
latest_data = {
    "rpm": 0,
    "coolant": 0, 
    "throttle": 0,
    "speed": 0
}

@app.route('/data')
def get_data():
    return jsonify(latest_data)

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
                    latest_data = json.loads(data)
        except Exception as e:
            print(f"WebSocket error: {e}")
            await asyncio.sleep(2)

            def calculate_gear(self, rpm, speed):
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

def run_websocket_client():
    asyncio.new_event_loop().run_until_complete(websocket_client())

if __name__ == "__main__":
    # Start WebSocket client in background thread
    ws_thread = threading.Thread(target=run_websocket_client, daemon=True)
    ws_thread.start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=8766, debug=False)