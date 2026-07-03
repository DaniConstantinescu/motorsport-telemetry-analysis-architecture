from prometheus_client import start_http_server, Histogram, Counter, Gauge

latency_metric = Histogram(
    "mqtt_message_latency_seconds",
    "End-to-end latency (device → server)",
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1)
)

pipeline_queue_size = Gauge(
    "edge_pipeline_queue_size",
    "Number of telemetry messages waiting in the edge processing queue"
)

pipeline_dropped_messages = Counter(
    "edge_pipeline_dropped_messages_total",
    "Number of telemetry messages dropped because the edge processing queue was full"
)

def start_metrics_server(port=8000):
    start_http_server(port)
    print(f"Prometheus metrics exposed on port {port}")
