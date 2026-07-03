import time
import random
from threading import Lock

class AnomalyDetector:
    def __init__(self, loki_logger, interval=100):
        self.interval = interval
        self.count = 0
        self.loki = loki_logger
        self.lock = Lock()

    def check(self, data, latency):
        with self.lock:
            self.count += 1
            message_count = self.count

        # 1. Start timer for real delta calculation
        start_time = time.time()

        # 2. Random distribution processing (10ms to 30ms)
        time.sleep(random.uniform(0.01, 0.03))
        proc_time = time.time() - start_time
        detection_timestamp = time.time()

        if message_count % self.interval == 0:
            # Trigger the Loki Alert
            self.loki.emit_anomaly_alert(data, latency, proc_time, detection_timestamp)

            # print(f"{time.time()} ⚠ ALERT: Anomaly found for device {data.get('device_id')} | Proc Time: {proc_time:.4f}s")
            return True

        return False
