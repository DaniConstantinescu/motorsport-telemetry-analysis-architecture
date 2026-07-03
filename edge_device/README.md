# Edge Device

`edge_device` simulates an edge device. It reads a CSV file row by row, adds timestamps to each message, and publishes telemetry through MQTT to the configured broker.

## Prerequisites

- Python 3.13 for local execution.
- Python dependencies from `requirements.txt`.
- A running MQTT broker, such as Mosquitto.
- A valid CSV file. The first two lines are treated as headers and units, and data rows are read starting from the third line.

## Configuration

The component reads configuration from environment variables:

```text
DATA_FILE     CSV file to read; default: data.csv
INTERVAL      delay between messages, in seconds; default: 0.005
MQTT_BROKER   MQTT broker host; default: localhost
MQTT_PORT     MQTT broker port; default: 1883
MQTT_TOPIC    MQTT topic; default: data/telemetry.csv
```

The `.env` file used by compose sets:

```text
DATA_FILE=/data/default.csv
MQTT_BROKER=mosquitto
MQTT_PORT=1883
MQTT_TOPIC=telemetry/line
INTERVAL=0.005
```

In `podman-compose.yaml`, `DATA_FILE` is overridden for each device instance.

## Run With Podman Compose

From the project root:

```bash
podman compose -f infrastructure/podman-compose.yaml up --build device1
```

## Local Execution

Start a local MQTT broker on `localhost:1883`, then:

```bash
cd edge_device
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```