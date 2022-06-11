import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

topic = "example-topic"


def on_connect(ctx: mqtt.Client, userdata, flags, rc, propertiesa):
    print("Connected with result code "+str(rc))

    ctx.subscribe(topic)
    client.publish(topic, "Hello from python!")


def on_message(ctx, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode('utf-8')}")


def on_connect_fail():
    print("Connection failed!")


def on_disconnect():
    print("Disconnected!")


client = mqtt.Client(protocol=mqtt.MQTTv5)

client.username_pw_set("anything", os.getenv("BROKER_TOKEN"))

client.tls_set()

client.connect(os.getenv("PUBSUB_URI"), int(os.getenv("PUBSUB_PORT")))
client.on_connect = on_connect
client.on_message = on_message
client.on_connect_fail = on_connect_fail
client.on_disconnect = on_disconnect

client.loop_forever()
