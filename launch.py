import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def start_services():
    services = [
        ("🌉 Data Bridge", "python/data_bridge.py"),
        ("📊 API Server", "python/api_server.py"), 
        ("📈 Data Logger", "python/data_logger.py"),
        ("🔧 Diagnostics", "python/diagnostics.py")
    ]
    
    for service_name, script_path in services:
        Thread(target=run_service, args=(service_name, script_path), daemon=True).start()
        time.sleep(1)

def show_system_status():
    print("\n" + "="*60)
    print("🚗 VEHICLE EASE PRO - ENTERPRISE EDITION")
    print("="*60)
    print("📊 Available Features:")
    print("  ✅ Real-time OBD-II Monitoring")
    print("  ✅ Pygame 3D Engine Visualization") 
    print("  ✅ Data Logging & Analytics")
    print("  ✅ RESTful API with Historical Data")
    print("  ✅ Smart Diagnostics & Alerts")
    print("  ✅ Progressive Web App (PWA)")
    print("  ✅ Mobile-First Dashboard")
    print("  ✅ Performance Analytics")
    print("\n🌐 Access Points:")
    print("  📱 Main Dashboard: http://localhost:8766/dashboard")
    print("  📊 Analytics: http://localhost:8766/analytics")
    print("  🔌 API Docs: http://localhost:8766/api/current")
    print("="*60)

if __name__ == "__main__":
    show_system_status()
    start_services()
    
    # Open dashboard
    time.sleep(3)
    webbrowser.open('http://localhost:8766/dashboard')
    
    input("\n🎯 Press Enter to stop all services...")