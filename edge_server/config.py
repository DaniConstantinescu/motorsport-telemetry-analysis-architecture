import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    mqtt_broker: str = "127.0.0.1"   # broker host for in-process broker
    mqtt_port: int = 1883             # broker port
    mqtt_topic: str = "telemetry/line"  # topic to subscribe
    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    queue_name: str = "telemetry"

def load_config() -> AppConfig:
    return AppConfig(
        mqtt_broker=os.getenv("MQTT_BROKER", "mosquitto"),
        mqtt_port=int(os.getenv("MQTT_PORT", "1883")),
        mqtt_topic=os.getenv("MQTT_TOPIC", "telemetry/line"),
        rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq"),
        rabbitmq_port = int(os.getenv("RABBITMQ_PORT", "5672")),
        queue_name = os.getenv("RABBITMQ_QUEUE", "telemetry")
    )
