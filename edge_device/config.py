import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    # CSV settings
    file_name: str = "data/telemetry.csv"
    interval: float = 0.01  # seconds

    # MQTT settings
    mqtt_broker: str = "localhost"
    mqtt_port: int = 1883
    mqtt_topic: str = "telemetry"

def load_config() -> AppConfig:
    """
    Load configuration from environment variables with defaults.
    """
    return AppConfig(
        file_name=os.getenv("DATA_FILE", "data.csv"),
        interval=float(os.getenv("INTERVAL", "0.005")),
        mqtt_broker=os.getenv("MQTT_BROKER", "localhost"),
        mqtt_port=int(os.getenv("MQTT_PORT", "1883")),
        mqtt_topic=os.getenv("MQTT_TOPIC", "data/telemetry.csv")
    )