import os, queue
from threading import Event
import paho.mqtt.client as mqtt

shutdown_event = Event()

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))

cmd_queue = queue.Queue()
paused_event = Event()

def on_connect(client, userdata, flags, rc):
    client.subscribe("assistant/cmd")

def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip()
    if payload == "shutdown":
        print("[MQTT] Shutdown signal received.")
        publish("assistant/state", "stopped")
        shutdown_event.set()

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

def stop_mqtt():
    c = mqtt_client()
    c.loop_stop()
    c.disconnect()
