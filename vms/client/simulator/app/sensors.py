import random
import json
import time
import os
import paho.mqtt.client as mqtt
from datetime import datetime
from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date  # дата рождения для формулы
        self.day = birth_date.day
        self.month = birth_date.month
        self.year = birth_date.year
        
    @abstractmethod
    def generate_value(self):
        pass
    
    def get_formatted_value(self, format_type, value):
        if format_type == "json":
            return json.dumps({"name": self.name, "value": round(value, 2)})
        else:
            return str(round(value, 2))

class TemperatureSensor(Sensor):
    def generate_value(self):
        # Базовая температура 20-30°C с влиянием даты рождения
        base = random.uniform(20, 30)
        # Влияние дня рождения (0-31) и месяца (1-12)
        influence = (self.day / 100) * (self.month / 12)
        return base + influence + random.uniform(-1, 1)

class PressureSensor(Sensor):
    def generate_value(self):
        # Давление 980-1050 hPa
        base = random.uniform(980, 1050)
        influence = (self.year % 100) / 100  # последние 2 цифры года
        return base + influence + random.uniform(-5, 5)

class CurrentSensor(Sensor):
    def generate_value(self):
        # Ток 0-15 A
        base = random.uniform(0, 15)
        influence = (self.month / 12) * self.day / 31
        return base + influence + random.uniform(-0.5, 0.5)

class HumiditySensor(Sensor):
    def generate_value(self):
        # Влажность 30-90%
        base = random.uniform(30, 90)
        influence = (self.day / 31) * 0.2
        return base + influence + random.uniform(-2, 2)