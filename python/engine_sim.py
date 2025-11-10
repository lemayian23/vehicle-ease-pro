import pygame
import math
import sys
import requests
import json
from pygame.locals import *

class EngineSimulator:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Vehicle Ease Pro - Engine Simulator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Engine state
        self.rpm = 0
        self.coolant_temp = 0
        self.throttle = 0
        self.speed = 0
        
        # Piston positions (V6 engine)
        self.pistons = [0, 120, 240, 60, 180, 300]  # degrees offset
        
    def fetch_data(self):
        """Get data from WebSocket server"""
        try:
            # For now, we'll simulate data. Replace with actual WebSocket connection
            # This would connect to your real_server.py or fake_server.py
            response = requests.get('http://localhost:8766/data')  # We'll create this endpoint
            if response.status_code == 200:
                data = response.json()
                self.rpm = data.get('rpm', 0)
                self.coolant_temp = data.get('coolant', 0)
                self.throttle = data.get('throttle', 0)
                self.speed = data.get('speed', 0)
        except:
            # Fallback to simulated data
            self.rpm = min(8000, self.rpm + 100 if self.throttle > 50 else max(800, self.rpm - 100))
            self.coolant_temp = 80 + (self.rpm / 8000 * 40)
            self.throttle = (self.throttle + 10) % 100
            self.speed = int(self.rpm * 0.02)

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
        
        # Speed
        speed_text = self.font.render(f"Speed: {self.speed} km/h", True, (0, 255, 0))
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
            self.draw_gauges()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    simulator = EngineSimulator()
    simulator.run()