import os
import json
import time
from threading import Lock
from datetime import datetime, timezone

from logger import LokiLogger
from rabbitmq_publisher import RabbitMQPublisher
from metrics import latency_metric
from anomaly_detector import AnomalyDetector


def add_latency_fields(data: dict) -> dict:
    """
    Adds latency fields (numeric + ISO) to telemetry data.
    Returns the updated dict.
    """

    # --- numeric timestamps (seconds) ---
    try:
        numeric_latency_s = float(data["edge_server_timestamp"]) - float(data["timestamp"])
        data["time_latency"] = numeric_latency_s
        data["time_latency_ms"] = numeric_latency_s * 1000
    except Exception as e:
        print(f"[LATENCY ERROR - numeric]: {e}")

    # --- ISO timestamps ---
    try:
        t1 = datetime.fromisoformat(data["timestamp_iso"])
        t2 = datetime.fromisoformat(data["edge_server_timestamp_iso"])

        iso_latency_s = (t2 - t1).total_seconds()
        data["time_latency_iso"] = iso_latency_s
        data["time_latency_iso_ms"] = iso_latency_s * 1000

    except Exception as e:
        print(f"[LATENCY ERROR - iso]: {e}")

    return data

class MessageProcessor:
    def __init__(self, log_file="/app/logs/telemetry.txt"):
        self.publisher = RabbitMQPublisher()
        self.loki = LokiLogger()
        self.anomaly_detector = AnomalyDetector(loki_logger=self.loki)
        self.file_lock = Lock()
        self.publisher_lock = Lock()

        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # CLEAN FILE ON STARTUP
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write("")


    def write_to_file(self, data):
        try:
            with self.file_lock:
                with open(self.log_file, "a", encoding="utf-8") as f:
                    f.write(f"{json.dumps(data)}\n")
        except Exception as e:
            print(f"[ERROR] Failed writing telemetry log: {e}")

    def process(self, data):
        if not isinstance(data, dict) or "timestamp" not in data:
            return

        # Calculate Latency
        latency = time.time() - float(data["timestamp"])
        latency_metric.observe(latency)

        data["edge_server_timestamp"] = time.time()
        data["edge_server_timestamp_iso"] = datetime.now(timezone.utc).isoformat()

        # print("Data in processor: ", data)
        data = add_latency_fields(data)
        self.write_to_file(data)

        # Detection logic (Alerting happens inside here now)
        self.anomaly_detector.check(data, latency)

        # Normal Flow
        with self.publisher_lock:
            self.publisher.publish_to_cloud(data)
