import os

from mqtt_listener import MQTTListener
from processor import MessageProcessor
from metrics import start_metrics_server
from message_pipeline import MessagePipeline

if __name__ == "__main__":
    start_metrics_server(8000)

    processor = MessageProcessor()
    pipeline = MessagePipeline(
        processor=processor,
        num_workers=int(os.getenv("EDGE_WORKERS", "10")),
        max_queue_size=int(os.getenv("EDGE_QUEUE_MAXSIZE", "10000")),
    )
    listener = MQTTListener(pipeline)

    listener.start()
