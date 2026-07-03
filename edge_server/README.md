# Edge Server

`edge_server` receives telemetry from devices through MQTT, processes messages in an internal worker-thread pipeline, computes latency values, runs a simple anomaly detection flow, and publishes the result to RabbitMQ for cloud consumption.

The component exposes Prometheus metrics on port `8000`.

## Prerequisites

- Python 3.13 for local execution.
- Python dependencies from `requirements.txt`.
- A running MQTT broker.
- A running RabbitMQ instance.
- For the full system, run it through Podman Compose as described in the root README.

## Configuration

Environment variables:

```text
MQTT_BROKER          MQTT broker host; default: mosquitto in config.py, 127.0.0.1 in the listener if unset
MQTT_PORT            MQTT broker port; default: 1883
MQTT_TOPIC           MQTT topic to subscribe to; default: telemetry/line
RABBITMQ_HOST        RabbitMQ host; default: rabbitmq
RABBITMQ_PORT        RabbitMQ port; default: 5672
RABBITMQ_QUEUE       RabbitMQ queue; default: telemetry
EDGE_WORKERS         number of worker threads; default: 10
EDGE_QUEUE_MAXSIZE   maximum internal queue size; default: 10000
```

The `.env` file sets the MQTT connection and RabbitMQ queue. In compose, `RABBITMQ_HOST` and `RABBITMQ_PORT` are explicitly overridden to use the `rabbitmq` service.

## Run With Podman Compose

From the project root:

```bash
podman compose -f infrastructure/podman-compose.yaml up --build edge_server
```

## Local Execution

Start Mosquitto and RabbitMQ locally, then:

```bash
cd edge_server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```

## Output

- Prometheus metrics: `http://localhost:8000`
- Processed telemetry log: `/app/logs/telemetry.txt` inside the container, mounted to `infrastructure/logs/telemetry.txt` by compose.
- Anomaly alert log: `infrastructure/logs/anomaly_alerts.log`.

The telemetry log file is cleared when the component starts.
