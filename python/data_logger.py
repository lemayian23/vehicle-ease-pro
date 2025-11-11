import json
import csv
import time
from datetime import datetime
import sqlite3

class DataLogger:
    def __init__(self):
        self.conn = sqlite3.connect('vehicle_data.db', check_same_thread=False)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trip_data (
                id INTEGER PRIMARY KEY,
                timestamp DATETIME,
                rpm INTEGER,
                speed INTEGER,
                coolant_temp INTEGER,
                throttle INTEGER,
                gear TEXT,
                fuel_consumption REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trip_summary (
                id INTEGER PRIMARY KEY,
                start_time DATETIME,
                end_time DATETIME,
                total_distance REAL,
                avg_speed REAL,
                max_speed INTEGER,
                fuel_used REAL,
                trip_duration INTEGER
            )
        ''')
        self.conn.commit()
    
    def log_data(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO trip_data 
            (timestamp, rpm, speed, coolant_temp, throttle, gear, fuel_consumption)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now(),
            data['rpm'],
            data['speed'],
            data['coolant'],
            data['throttle'],
            data.get('gear', 'N'),
            self.calculate_fuel_consumption(data)
        ))
        self.conn.commit()
    
    def calculate_fuel_consumption(self, data):
        # Simple fuel calculation based on RPM and throttle
        base_consumption = 0.0002  # liters per second at idle
        rpm_factor = data['rpm'] / 1000 * 0.001
        throttle_factor = data['throttle'] / 100 * 0.002
        return base_consumption + rpm_factor + throttle_factor
    
    def get_trip_statistics(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                COUNT(*) as data_points,
                AVG(speed) as avg_speed,
                MAX(speed) as max_speed,
                SUM(fuel_consumption) as total_fuel,
                MIN(timestamp) as start_time,
                MAX(timestamp) as end_time
            FROM trip_data 
            WHERE date(timestamp) = date('now')
        ''')
        return cursor.fetchone()