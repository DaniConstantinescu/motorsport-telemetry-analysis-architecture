# Team Cloud

`team_cloud` is the cloud component of the system. It consumes processed messages from RabbitMQ, adds cloud timestamps, computes end-to-end latency, writes telemetry to a file, and exposes Prometheus metrics.

The component exposes metrics on port `8100`.

## Prerequisites

- Python 3.11 for local execution.
- Python dependencies from `requirements.txt`.
- A running RabbitMQ instance.
- For the full system, run it through Podman Compose as described in the root README.

## Configuration

Environment variables:

```text
RABBITMQ_HOST    RabbitMQ host; default: localhost in config.py
RABBITMQ_PORT    RabbitMQ port; default: 5672
RABBITMQ_QUEUE   RabbitMQ queue; default: telemetry
```

The `.env` file sets:

```text
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_QUEUE=telemetry
```

## Run With Podman Compose

From the project root:

```bash
podman compose -f infrastructure/podman-compose.yaml up --build team_cloud
```

## Local Execution

Start RabbitMQ and make sure the configured host is reachable, then:

```bash
cd team_cloud
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python main.py
```

## Output

- Prometheus metrics: `http://localhost:8100`
- Cloud telemetry log: `/app/logs/cloud_telemetry.txt` inside the container, mounted to `infrastructure/logs/cloud_telemetry.txt` by compose.

The cloud telemetry log file is cleared when the component starts.
