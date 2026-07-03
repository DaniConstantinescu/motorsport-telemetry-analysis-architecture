import paho.mqtt.client as mqtt
import json


class MQTTSender:
    def __init__(self, broker_host='localhost', broker_port=1883, client_id=None, username=None, password=None):
        # Force callback API version 1 (compatible with Python 3.13)
        self.client = mqtt.Client(client_id=client_id, callback_api_version=1)

        if username and password:
            self.client.username_pw_set(username, password)

        self.client.connect(broker_host, broker_port)

    def send(self, topic, message):
        if isinstance(message, dict):
            message = json.dumps(message)
        self.client.publish(topic, message)

    def disconnect(self):
        self.client.disconnect()