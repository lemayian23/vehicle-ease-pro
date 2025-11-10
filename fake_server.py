# fake_server.py  ← 100% WORKING FAKE DATA (NO OBD NEEDED)
import asyncio
import websockets
import json
import math
import time

async def fake_obd(websocket, path):
    print("Phone connected! Sending fake live data...")
    start_time = time.time()
    
    while True:
        t = time.time() - start_time
        rpm = 800 + 6000 * abs(math.sin(t / 3))
        throttle = 15 + 85 * abs(math.sin(t / 3))
        speed = rpm * 0.05 + 20 * math.sin(t / 2)
        coolant = 85 + 15 * math.sin(t / 10)
        
        data = {
            "rpm": int(rpm),
            "coolant": int(coolant),
            "throttle": int(throttle),
            "speed": int(speed),
        }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(0.05)

start_server = websockets.serve(fake_obd, "0.0.0.0", 8765)
print("FAKE SERVER RUNNING ON ws://YOUR_IP:8765")
print("Find your IP below ↓")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()