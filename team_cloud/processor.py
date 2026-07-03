import os
import time
import json
from threading import Lock
from datetime import datetime, timezone

from metrics import cloud_latency_metric, cloud_messages_processed

def add_latency_fields(data: dict) -> dict:
    """
    Adds latency fields (numeric + ISO) to telemetry data.
    Returns the updated dict.
    """

    # --- numeric timestamps (seconds) ---
    try:
        numeric_latency_s = float(data["cloud_timestamp"]) - float(data["timestamp"])
        data["cloud_time_latency"] = numeric_latency_s
        data["cloud_time_latency_ms"] = numeric_latency_s * 1000
    except Exception as e:
        print(f"[LATENCY ERROR - numeric]: {e}")

    # --- ISO timestamps ---
    try:
        t1 = datetime.fromisoformat(data["timestamp_iso"])
        t2 = datetime.fromisoformat(data["cloud_timestamp_iso"])

        iso_latency_s = (t2 - t1).total_seconds()
        data["time_latency_iso"] = iso_latency_s
        data["time_latency_iso_ms"] = iso_latency_s * 1000

    except Exception as e:
        print(f"[LATENCY ERROR - iso]: {e}")

    return data

class Processor:
    def __init__(self, log_file="/app/logs/cloud_telemetry.txt"):
        self.file_lock = Lock()
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

    def process_message(self,  data: dict):
        data["cloud_timestamp"] = time.time()
        data["cloud_timestamp_iso"] = datetime.now(timezone.utc).isoformat()

        data = add_latency_fields(data)

        if "cloud_time_latency" in data:
            cloud_latency_metric.observe(data["cloud_time_latency"])
        cloud_messages_processed.inc()

        self.write_to_file(data)

        print(f"[PROCESS] Received: {data}")
