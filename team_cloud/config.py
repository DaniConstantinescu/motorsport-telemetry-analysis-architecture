import os
from dataclasses import dataclass

@dataclass
class Config:
    rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "localhost")
    rabbitmq_port: int = int(os.getenv("RABBITMQ_PORT", 5672))
    rabbitmq_queue: str = os.getenv("RABBITMQ_QUEUE", "telemetry")

config = Config()