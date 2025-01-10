import time
import random
import numpy as np
from datetime import datetime

class SensorSimulator:
    def __init__(self):
        self.machine_states = {
            'healthy': {'temp_range': (60, 75), 'vibration_range': (0.5, 1.5)},
            'warning': {'temp_range': (76, 85), 'vibration_range': (1.6, 2.5)},
            'critical': {'temp_range': (86, 100), 'vibration_range': (2.6, 4.0)}
        }
        self.current_state = 'healthy'
        self.degradation_factor = 0.0

    def generate_sensor_data(self):
        # Increase degradation over time
        self.degradation_factor += random.uniform(0, 0.01)
        
        # Potentially change state based on degradation
        if self.degradation_factor > 0.7:
            self.current_state = 'critical'
        elif self.degradation_factor > 0.4:
            self.current_state = 'warning'
            
        state_ranges = self.machine_states[self.current_state]
        
        # Generate sensor readings with some random noise
        temperature = random.uniform(*state_ranges['temp_range']) + (self.degradation_factor * 10)
        vibration = random.uniform(*state_ranges['vibration_range']) + (self.degradation_factor)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'temperature': round(temperature, 2),
            'vibration': round(vibration, 2),
            'state': self.current_state,
            'degradation': round(self.degradation_factor, 3)
        }

    def reset(self):
        self.current_state = 'healthy'
        self.degradation_factor = 0.0