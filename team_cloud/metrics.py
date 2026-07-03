from prometheus_client import Counter, Histogram, start_http_server


cloud_latency_metric = Histogram(
    "team_cloud_message_latency_seconds",
    "End-to-end latency from device timestamp to team cloud processing",
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1),
)

cloud_messages_processed = Counter(
    "team_cloud_messages_processed_total",
    "Number of telemetry messages processed by the team cloud",
)


def start_metrics_server(port=8100):
    start_http_server(port)
    print(f"Team cloud Prometheus metrics exposed on port {port}")
