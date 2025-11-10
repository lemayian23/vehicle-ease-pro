# real_server.py  ← USE THIS WHEN YOU HAVE THE DONGLE
import asyncio
import websockets
import json
import obd

async def real_obd(websocket, path):
    connection = obd.OBD()
    if not connection.is_connected():
        await websocket.send(json.dumps({"error": "No car connected"}))
        return
    
    print("REAL CAR CONNECTED! Streaming live data...")
    while True:
        rpm = connection.query(obd.commands.RPM)
        coolant = connection.query(obd.commands.COOLANT_TEMP)
        throttle = connection.query(obd.commands.THROTTLE_POS)
        speed = connection.query(obd.commands.SPEED)

        data = {
            "rpm": int(rpm.value.magnitude) if rpm.value else 0,
            "coolant": int(coolant.value.to("degC").magnitude) if coolant.value else 0,
            "throttle": int(throttle.value.magnitude) if throttle.value else 0,
            "speed": int(speed.value.to("km/h").magnitude) if speed.value else 0,
        }
        await websocket.send(json.dumps(data))
        await asyncio.sleep(0.05)

start_server = websockets.serve(real_obd, "0.0.0.0", 8765)
print("REAL OBD SERVER RUNNING")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()