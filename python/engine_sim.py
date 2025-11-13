import pygame
import math
import sys
import requests
import json
from pygame.locals import *

class EngineSimulator:
    def __init__(self):
        pygame.init()
        self.width, self.height = 900, 600  # Increased width for gear display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Vehicle Ease Pro - Engine Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Engine state
        self.rpm = 0
        self.coolant_temp = 0
        self.throttle = 0
        self.speed = 0
        self.gear = "N"  # N, 1, 2, 3, 4, 5, 6, R
        
        # Piston positions (V6 engine)
        self.pistons = [0, 120, 240, 60, 180, 300]  # degrees offset
        
        # Gear ratios (typical manual transmission)
        self.gear_ratios = {
            "R": -3.5, "1": 3.8, "2": 2.2, "3": 1.5, 
            "4": 1.1, "5": 0.8, "6": 0.6
        }

  def draw_fuel_display(self):
    """Draw fuel efficiency information"""
    # Fuel display background
    pygame.draw.rect(self.screen, (20, 20, 20), (650, 270, 200, 120), border_radius=15)
    pygame.draw.rect(self.screen, (0, 100, 0), (650, 270, 200, 120), 3, border_radius=15)
    
    # Fuel efficiency
    efficiency = max(0, self.speed / max(1, self.rpm/500))  # Simplified calculation
    efficiency_text = self.font.render(f"{efficiency:.1f} km/L", True, (0, 255, 0))
    efficiency_rect = efficiency_text.get_rect(center=(750, 300))
    self.screen.blit(efficiency_text, efficiency_rect)
    
    # Fuel rate
    fuel_rate = 0.8 + (self.rpm / 1000 * 0.5) + (self.throttle / 100 * 1.2)
    rate_text = self.small_font.render(f"Fuel: {fuel_rate:.1f} L/h", True, (100, 255, 100))
    rate_rect = rate_text.get_rect(center=(750, 330))
    self.screen.blit(rate_text, rate_rect)
    
    # Efficiency status
    if efficiency > 15:
        status = "EXCELLENT"
        color = (0, 255, 0)
    elif efficiency > 10:
        status = "GOOD"
        color = (255, 200, 0)
    elif efficiency > 5:
        status = "POOR"
        color = (255, 100, 0)
    else:
        status = "VERY POOR"
        color = (255, 0, 0)
    
    status_text = self.small_font.render(status, True, color)
    status_rect = status_text.get_rect(center=(750, 360))
    self.screen.blit(status_text, status_rect) 

    self.draw_fuel_display()  # Add this line     
        
    def calculate_gear(self):
        """Calculate current gear based on RPM and speed"""
        if self.speed == 0 or self.rpm < 500:
            return "N"
        
        # Simple gear calculation based on RPM/speed ratio
        ratio = self.rpm / max(1, self.speed)
        
        # Find closest matching gear
        closest_gear = "N"
        min_diff = float('inf')
        
        for gear, gear_ratio in self.gear_ratios.items():
            if gear == "R":  # Skip reverse for forward motion
                continue
            diff = abs(ratio - gear_ratio * 100)  # Scale factor
            if diff < min_diff:
                min_diff = diff
                closest_gear = gear
        
        return closest_gear

    def fetch_data(self):
        """Get data from WebSocket server"""
        try:
            response = requests.get('http://localhost:8766/data')
            if response.status_code == 200:
                data = response.json()
                self.rpm = data.get('rpm', 0)
                self.coolant_temp = data.get('coolant', 0)
                self.throttle = data.get('throttle', 0)
                self.speed = data.get('speed', 0)
                self.gear = self.calculate_gear()
        except:
            # Fallback to simulated data with gear calculation
            self.rpm = min(8000, self.rpm + 100 if self.throttle > 50 else max(800, self.rpm - 100))
            self.coolant_temp = 80 + (self.rpm / 8000 * 40)
            self.throttle = (self.throttle + 10) % 100
            self.speed = int(self.rpm * 0.02)
            self.gear = self.calculate_gear()

    def draw_engine_block(self):
        """Draw the engine block"""
        # Engine block
        pygame.draw.rect(self.screen, (100, 100, 100), (200, 150, 400, 200), border_radius=10)
        
        # Cylinder banks (V6)
        for i in range(3):
            # Left bank
            pygame.draw.rect(self.screen, (80, 80, 80), (250, 160 + i*60, 30, 40))
            # Right bank  
            pygame.draw.rect(self.screen, (80, 80, 80), (520, 160 + i*60, 30, 40))

    def draw_pistons(self):
        """Draw moving pistons based on RPM"""
        if self.rpm == 0:
            return
            
        time_ms = pygame.time.get_ticks()
        cycle_time = 60000 / max(1, self.rpm)  # ms per revolution
        
        for i, offset in enumerate(self.pistons):
            angle = ((time_ms / cycle_time * 360) + offset) % 360
            piston_y = 200 + math.sin(math.radians(angle)) * 30
            
            # Determine bank position
            if i < 3:  # Left bank
                x_pos = 265
                y_pos = 180 + i*60
            else:  # Right bank
                x_pos = 535
                y_pos = 180 + (i-3)*60
            
            # Piston
            pygame.draw.rect(self.screen, (200, 200, 100), (x_pos-10, piston_y, 20, 15))
            # Connecting rod
            pygame.draw.line(self.screen, (150, 150, 150), (x_pos, y_pos), (x_pos, piston_y), 3)

    def draw_exhaust(self):
        """Draw exhaust flames based on RPM and throttle"""
        if self.rpm > 3000 and self.throttle > 70:
            flame_intensity = min(1.0, (self.rpm - 3000) / 5000)
            
            # Left exhaust
            for i in range(3):
                flame_height = 20 + flame_intensity * 30
                flame_width = 10 + flame_intensity * 10
                points = [
                    (240, 350 + i*20),
                    (240 - flame_width, 350 + i*20 + flame_height),
                    (240 + flame_width, 350 + i*20 + flame_height)
                ]
                color = (255, 100, 0) if flame_intensity > 0.7 else (255, 200, 0)
                pygame.draw.polygon(self.screen, color, points)
            
            # Right exhaust
            for i in range(3):
                flame_height = 20 + flame_intensity * 30
                flame_width = 10 + flame_intensity * 10
                points = [
                    (560, 350 + i*20),
                    (560 - flame_width, 350 + i*20 + flame_height),
                    (560 + flame_width, 350 + i*20 + flame_height)
                ]
                color = (255, 100, 0) if flame_intensity > 0.7 else (255, 200, 0)
                pygame.draw.polygon(self.screen, color, points)

    def draw_digital_speedometer(self):
        """Draw digital speedometer with gear indicator"""
        # Speed display background
        pygame.draw.rect(self.screen, (20, 20, 20), (650, 100, 200, 150), border_radius=15)
        pygame.draw.rect(self.screen, (0, 100, 0), (650, 100, 200, 150), 3, border_radius=15)
        
        # Speed value
        speed_text = self.font.render(f"{self.speed}", True, (0, 255, 0))
        speed_rect = speed_text.get_rect(center=(750, 150))
        self.screen.blit(speed_text, speed_rect)
        
        # Speed unit
        unit_text = self.small_font.render("km/h", True, (100, 255, 100))
        unit_rect = unit_text.get_rect(center=(750, 180))
        self.screen.blit(unit_text, unit_rect)
        
        # Gear indicator
        gear_bg_color = (0, 100, 0) if self.gear != "N" else (100, 100, 0)
        pygame.draw.rect(self.screen, gear_bg_color, (700, 200, 100, 40), border_radius=10)
        
        gear_text = self.font.render(self.gear, True, (255, 255, 255))
        gear_rect = gear_text.get_rect(center=(750, 220))
        self.screen.blit(gear_text, gear_rect)
        
        # Gear label
        gear_label = self.small_font.render("GEAR", True, (150, 150, 150))
        gear_label_rect = gear_label.get_rect(center=(750, 240))
        self.screen.blit(gear_label, gear_label_rect)

    def draw_gauges(self):
        """Draw digital gauges"""
        # RPM
        rpm_text = self.font.render(f"RPM: {self.rpm}", True, (0, 255, 0))
        self.screen.blit(rpm_text, (50, 450))
        
        # Coolant
        coolant_text = self.font.render(f"Coolant: {self.coolant_temp}°C", True, (0, 255, 0))
        self.screen.blit(coolant_text, (50, 490))
        
        # Throttle
        throttle_text = self.font.render(f"Throttle: {self.throttle}%", True, (0, 255, 0))
        self.screen.blit(throttle_text, (50, 530))
        
        # Speed (smaller - main display is in speedometer)
        speed_text = self.small_font.render(f"Speed: {self.speed} km/h", True, (100, 255, 100))
        self.screen.blit(speed_text, (400, 530))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.throttle = min(100, self.throttle + 10)
                    elif event.key == K_DOWN:
                        self.throttle = max(0, self.throttle - 10)
                    elif event.key == K_ESCAPE:
                        running = False
            
            self.fetch_data()
            self.screen.fill((0, 0, 0))
            
            self.draw_engine_block()
            self.draw_pistons()
            self.draw_exhaust()
            self.draw_digital_speedometer()
            self.draw_gauges()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    simulator = EngineSimulator()
    simulator.run()