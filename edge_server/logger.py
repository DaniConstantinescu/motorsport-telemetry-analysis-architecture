import logging
import json
import os


class LokiLogger:
    def __init__(self, log_file="/logs/anomaly_alerts.log"):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        self.logger = logging.getLogger("anomaly_logger")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file, mode="w")
            file_handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(file_handler)

    def emit_anomaly_alert(self, data, latency, proc_time, detection_timestamp):
        payload = {
            "alert_level": "CRITICAL",
            "event": "anomaly_detected",
            "device_id": data.get("device_id", "unknown"),
            "latency": round(latency, 6),
            "proc_time": round(proc_time, 6),
            "detection_timestamp": detection_timestamp,
            "detection_time_ms": latency * 1000 + proc_time * 1000,
            "msg_timestamp": data.get("timestamp")
        }

        print("logging for anomaly alert")
        print(json.dumps(payload))

        self.logger.info(json.dumps(payload))
