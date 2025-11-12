from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/api/current', methods=['GET'])
def get_current_data():
    """Get current vehicle data"""
    return jsonify(latest_data)

@app.route('/api/history', methods=['GET'])
def get_historical_data():
    """Get historical data for charts"""
    hours = request.args.get('hours', 1, type=int)
    
    conn = sqlite3.connect('vehicle_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT timestamp, rpm, speed, coolant_temp, throttle, gear
        FROM trip_data 
        WHERE timestamp > datetime('now', ?)
        ORDER BY timestamp
    ''', (f'-{hours} hours',))
    
    data = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'timestamp': row[0],
        'rpm': row[1],
        'speed': row[2],
        'coolant': row[3],
        'throttle': row[4],
        'gear': row[5]
    } for row in data])

@app.route('/api/trip/summary', methods=['GET'])
def get_trip_summary():
    """Get trip summary statistics"""
    conn = sqlite3.connect('vehicle_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            COUNT(*) as points,
            AVG(speed) as avg_speed,
            MAX(speed) as max_speed,
            SUM(fuel_consumption) as fuel_used,
            MIN(timestamp) as start_time,
            MAX(timestamp) as end_time
        FROM trip_data 
        WHERE date(timestamp) = date('now')
    ''')
    
    result = cursor.fetchone()
    conn.close()
    
    return jsonify({
        'data_points': result[0],
        'average_speed': round(result[1] or 0, 1),
        'max_speed': result[2] or 0,
        'fuel_used_liters': round(result[3] or 0, 3),
        'trip_duration_minutes': self.calculate_duration(result[4], result[5])
    })

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get current alerts"""
    return jsonify(diagnostics.alerts)

@app.route('/api/health', methods=['GET'])
def get_health_score():
    """Get vehicle health score"""
    return jsonify({'health_score': diagnostics.get_health_score(latest_data)})