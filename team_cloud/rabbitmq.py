import time
import pika
import json
from pika.exceptions import AMQPConnectionError
from config import config


def create_connection():
    while True:
        try:
            print("[INFO] Trying to connect to RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="rabbitmq")
            )
            print("[INFO] Connected to RabbitMQ")
            return connection
        except AMQPConnectionError:
            print("[WARN] RabbitMQ not ready, retrying in 5s...")
            time.sleep(5)

def start_consumer(processor):
    connection = create_connection()

    channel = connection.channel()
    channel.queue_declare(queue=config.rabbitmq_queue)

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            processor.process_message(message)
        except Exception as e:
            print(f"[ERROR] Failed processing message: {e}")

    channel.basic_consume(
        queue=config.rabbitmq_queue,
        on_message_callback=callback,
        auto_ack=True
    )

    print("[*] Waiting for messages...")
    channel.start_consuming()