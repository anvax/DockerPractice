import os
import time
import random
import paho.mqtt.client as mqtt
from datetime import datetime
from sensor import TemperatureSensor, PressureSensor, CurrentSensor, HumiditySensor

def main():
    # Чтение переменных окружения
    mqtt_host = os.getenv('MQTT_HOST', 'localhost')
    mqtt_port = int(os.getenv('MQTT_PORT', 1883))
    sensor_type = os.getenv('SENSOR_TYPE', 'temperature')
    sensor_name = os.getenv('SENSOR_NAME', 'sensor1')
    interval = int(os.getenv('PUBLISH_INTERVAL', 5))
    topic_format = os.getenv('TOPIC_FORMAT', 'json')  # 'json' или 'raw'
    birth_date_str = os.getenv('BIRTH_DATE', '1990-01-01')
    
    # Парсинг даты рождения
    birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
    
    # Создание датчика
    sensor_classes = {
        'temperature': TemperatureSensor,
        'pressure': PressureSensor,
        'current': CurrentSensor,
        'humidity': HumiditySensor
    }
    
    if sensor_type not in sensor_classes:
        raise ValueError(f"Unknown sensor type: {sensor_type}")
    
    sensor = sensor_classes[sensor_type](sensor_name, birth_date)
    
    # MQTT настройка
    client = mqtt.Client()
    client.connect(mqtt_host, mqtt_port, 60)
    
    print(f"Starting {sensor_type} sensor '{sensor_name}'")
    print(f"Publishing to {mqtt_host}:{mqtt_port} every {interval}s")
    
    try:
        while True:
            value = sensor.generate_value()
            
            if topic_format == 'json':
                # JSON формат: /sensors/type
                topic = f"/sensors/{sensor_type}"
                payload = f'{{"name":"{sensor_name}", "value":{value:.2f}}}'
            else:
                # Raw формат: /sensors/type/value
                topic = f"/sensors/{sensor_type}/{sensor_name}"
                payload = f"{value:.2f}"
            
            client.publish(topic, payload)
            print(f"[{sensor_name}] {topic}: {payload}")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("Stopping sensor...")
        client.disconnect()

if __name__ == "__main__":
    main()
