import pika
import json
import time
from config import load_config
from pika.exceptions import AMQPConnectionError, AMQPError

class RabbitMQPublisher:
    def __init__(self, host=None, queue=None):
        config = load_config()
        self.host = host or config.rabbitmq_host
        self.port = config.rabbitmq_port
        self.queue = queue or config.queue_name
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        """Create a persistent connection to RabbitMQ with retry."""
        while True:
            try:
                print(f"[INFO] Trying to connect to RabbitMQ at {self.host}:{self.port}...")
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, port=self.port)
                )
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queue)
                print("[INFO] Connected to RabbitMQ")
                break
            except AMQPConnectionError:
                print("[WARN] RabbitMQ not ready, retrying in 5s...")
                time.sleep(5)

    def publish_to_cloud(self, data: dict):
        """Publish a message to RabbitMQ, adding edge timestamp."""
        if not self.connection or self.connection.is_closed:
            print("[INFO] Connection closed, reconnecting...")
            self._connect()

        # Add edge timestamp
        data["edge_ingest_timestamp"] = time.time()

        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=json.dumps(data)
            )
            # print(f"[INFO] Message pushed to queue {self.queue}")
        except AMQPError as e:
            print(f"[ERROR] Failed to push message: {e}")
            # optionally try reconnect once
            self._connect()
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=json.dumps(data)
            )
            print(f"[INFO] Message pushed to queue {self.queue} after reconnect")
