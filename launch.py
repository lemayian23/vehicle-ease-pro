import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def start_server(script_name):
    """Start a Python script as subprocess"""
    try:
        if script_name == "fake_server.py":
            print("🚗 Starting FAKE OBD-II Server (no hardware needed)")
        else:
            print("🚗 Starting REAL OBD-II Server (requires OBD dongle)")
        
        subprocess.run([sys.executable, script_name])
    except Exception as e:
        print(f"Error starting {script_name}: {e}")

def start_engine_sim():
    """Start the Pygame engine simulator"""
    try:
        print("🎮 Starting Engine Simulator...")
        subprocess.run([sys.executable, "python/engine_sim.py"])
    except Exception as e:
        print(f"Error starting engine simulator: {e}")

def start_data_bridge():
    """Start the data bridge server"""
    try:
        print("🌉 Starting Data Bridge Server...")
        subprocess.run([sys.executable, "python/data_bridge.py"])
    except Exception as e:
        print(f"Error starting data bridge: {e}")

def open_dashboard():
    """Open the web dashboard in browser"""
    time.sleep(3)  # Give servers time to start
    try:
        webbrowser.open('http://localhost:8766/static/index.html')
        print("📱 Dashboard should open in your browser automatically!")
        print("📱 If not, manually open: dashboard/index.html")
    except:
        print("📱 Please manually open: dashboard/index.html")

if __name__ == "__main__":
    print("=" * 50)
    print("🚗 VEHICLE EASE PRO - MVP LAUNCHER")
    print("=" * 50)
    
    # Create necessary folders
    os.makedirs("python", exist_ok=True)
    os.makedirs("dashboard", exist_ok=True)
    
    print("\nChoose mode:")
    print("1. FAKE DATA (no OBD dongle needed) - Recommended for testing")
    print("2. REAL OBD (requires OBD-II Bluetooth dongle)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        # Start fake server
        server_thread = Thread(target=start_server, args=("fake_server.py",))
        server_thread.daemon = True
        server_thread.start()
    elif choice == "2":
        # Start real server  
        server_thread = Thread(target=start_server, args=("real_server.py",))
        server_thread.daemon = True
        server_thread.start()
    else:
        print("Invalid choice. Starting with fake data.")
        server_thread = Thread(target=start_server, args=("fake_server.py",))
        server_thread.daemon = True
        server_thread.start()
    
    # Start data bridge
    bridge_thread = Thread(target=start_data_bridge)
    bridge_thread.daemon = True
    bridge_thread.start()
    
    # Open dashboard
    dashboard_thread = Thread(target=open_dashboard)
    dashboard_thread.daemon = True
    dashboard_thread.start()
    
    print("\n🎯 All systems starting...")
    print("💡 Press Ctrl+C to stop all servers")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Vehicle Ease Pro...")