import os, queue
from threading import Event
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))

cmd_queue = queue.Queue()
paused_event = Event()

def on_connect(client, userdata, flags, rc):
    client.subscribe("assistant/cmd")

def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip()
    if payload == "pause":
        paused_event.set()
    elif payload == "resume":
        paused_event.clear()
    elif payload.startswith("say:"):
        cmd_queue.put(("say", payload[4:].strip()))

_client = None
def mqtt_client():
    global _client
    if _client: return _client
    c = mqtt.Client()
    c.on_connect = on_connect
    c.on_message = on_message
    c.connect(BROKER, PORT, 60)
    c.loop_start()
    _client = c
    return _client

def publish(topic, payload):
    mqtt_client().publish(topic, payload, qos=0, retain=False)
