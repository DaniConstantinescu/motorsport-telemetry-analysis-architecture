# Motorsport Telemetry System Template

**Motorsport Telemetry System Template** is a starting point for a distributed system for simulating, collecting, processing, and observing telemetry data produced by edge devices. The project has three main components:

- `edge_device`: simulates an edge device by replaying CSV files and publishing telemetry through MQTT.
- `edge_server`: consumes MQTT messages, computes latency values, runs a simple anomaly detection flow, writes logs, and forwards data to RabbitMQ.
- `team_cloud`: consumes data from RabbitMQ, computes end-to-end cloud latency, writes logs, and exposes Prometheus metrics.

The Podman Compose infrastructure also starts Mosquitto(MQTT Broker), RabbitMQ, Prometheus, Loki, Promtail, and Grafana.

## Architecture Overview

The main data flow is:

```text
edge_device -> MQTT/Mosquitto -> edge_server -> RabbitMQ -> team_cloud
                                      |                         |
                                      v                         v
                                 logs/metrics              logs/metrics
                                      |                         |
                                      v                         v
                                 Promtail/Loki          Prometheus/Grafana
```

The edge devices read CSV files from `infrastructure/data` and publish each row to the configured MQTT topic. `edge_server` listens to that MQTT topic, processes messages with worker threads, writes processed telemetry to `infrastructure/logs/telemetry.txt`, periodically emits anomaly alerts to `infrastructure/logs/anomaly_alerts.log`, and publishes messages to RabbitMQ. `team_cloud` consumes the RabbitMQ queue and writes the final processed data to `infrastructure/logs/cloud_telemetry.txt`.

## Prerequisites

- Podman installed.
- Support for `podman compose` or the standalone `podman-compose` utility.
- Access to the public images used by the compose file: `rabbitmq:3-management`, `prom/prometheus`, `grafana/loki`, `grafana/promtail`, `grafana/grafana`, and the Python images used during builds.
- Free local ports:
  - `1883` for Mosquitto MQTT
  - `5672` for RabbitMQ
  - `15672` for RabbitMQ Management UI
  - `3000` for Grafana
  - `9090` for Prometheus
  - `3100` for Loki
  - `8100` for `team_cloud` metrics

For local execution without containers, Python 3.11 is also required.

## Start With Podman Compose

From the project root:

```bash
podman compose -f infrastructure/podman-compose.yaml up --build
```

To start in the background:

```bash
podman compose -f infrastructure/podman-compose.yaml up --build -d
```

To stop the stack:

```bash
podman compose -f infrastructure/podman-compose.yaml down
```

To stop the stack and remove compose-created volumes:

```bash
podman compose -f infrastructure/podman-compose.yaml down -v
```

## Exposed Services

- Grafana: `http://localhost:3000`
  - username: `admin`
  - password: `admin`
- Prometheus: `http://localhost:9090`
- RabbitMQ Management: `http://localhost:15672`
- Loki: `http://localhost:3100`
- Mosquitto MQTT: `localhost:1883`

In compose, Prometheus scrapes metrics from:

- `edge_server:8000`
- `team_cloud:8100`

Grafana is provisioned with the Prometheus datasource and dashboards from `infrastructure/grafana`.

In compose, `edge_server` explicitly overrides `RABBITMQ_HOST=rabbitmq` and `RABBITMQ_PORT=5672`.

## Toxiproxy and Artificial Latency

`infrastructure/podman-compose.yaml` also contains a Toxiproxy configuration. It can be used to introduce artificial latency between `edge_server` and RabbitMQ. In the current configuration, the Toxiproxy services are commented out, and `edge_server` communicates directly with the `rabbitmq` service.

There is also an `infrastructure/.env` file with latency and jitter values

## Running Components Individually

The recommended way to run the full system is Podman Compose, because it starts all required external services. For development purposes, the system can also be run local component-by-component. Start Mosquitto and RabbitMQ first, then install each component's dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r edge_device/requirements.txt
pip install -r edge_server/requirements.txt
pip install -r team_cloud/requirements.txt
```

Then run each component from its own directory with the proper environment variables. See the component README files:

- `edge_device/README.md`
- `edge_server/README.md`
- `team_cloud/README.md`