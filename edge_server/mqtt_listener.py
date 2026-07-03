import os
import json
import paho.mqtt.client as mqtt

class MQTTListener:
    def __init__(self, pipeline, broker=None, port=None, topic=None):
        self.pipeline = pipeline

        self.broker = broker or os.getenv("MQTT_BROKER", "127.0.0.1")
        self.port = port or int(os.getenv("MQTT_PORT", "1883"))
        self.topic = topic or os.getenv("MQTT_TOPIC", "telemetry/line")

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to {self.broker}:{self.port}")
            client.subscribe(self.topic)
        else:
            print(f"Connection failed: {rc}")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()

        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return

        self.pipeline.submit(data)

    def start(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_forever()
