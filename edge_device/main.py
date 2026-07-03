import csv
import time
import sys
from datetime import datetime, timezone

from mqtt_sender import MQTTSender
from config import load_config

# -----------------------------
# Load configuration
# -----------------------------
config = load_config()

# Initialize MQTT
mqtt_sender = MQTTSender(broker_host=config.mqtt_broker, broker_port=config.mqtt_port)

# -----------------------------
# CSV replay function
# -----------------------------
def replay_file_fixed_interval(file_name, interval, max_lines=None):
    try:
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # skip header row
            units = next(reader)    # skip units row if present

            index = 0
            for row in reader:
                if len(row) == 0:
                    continue
                print(row)

                # Send via MQTT
                if mqtt_sender:
                    data = {headers[i]: row[i] for i in range(len(headers))}
                    data["timestamp"] = str(time.time())
                    data["timestamp_iso"] = datetime.now(timezone.utc).isoformat()
                    mqtt_sender.send(config.mqtt_topic, data)

                time.sleep(interval)
                index += 1

                if max_lines and index >= max_lines:
                    print("Max lines reached, exiting.")
                    sys.exit(0)

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print(f"Using file: {config.file_name}, interval: {config.interval}s")
    print(f"MQTT broker: {config.mqtt_broker}:{config.mqtt_port}")
    replay_file_fixed_interval(config.file_name, config.interval)