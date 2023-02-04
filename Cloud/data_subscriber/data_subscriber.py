import json
import time
from paho.mqtt import client as mqtt_client
from data_processor import process_data

sensor_data = []

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT OK!", flush=True)
    else:
        print("Failed to connect, return code %d\n", rc, flush=True)

# Callback function will be triggered
def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    if data != "end":
        split_data = data.split(",")
        sensor_data.append(split_data)
    else:
        client.disconnect()

def mqtt_subscriber():
    mqtt_ip="mqtt-broker"
    mqtt_port=1883
    topic = "CSC8112"

    # Create a mqtt client object
    client = mqtt_client.Client()

    # Connect to MQTT service
    client.on_connect = on_connect
    while True:
        try:
            print("Trying to connect", flush=True)
            client.connect(mqtt_ip, mqtt_port)
            break
        except ConnectionRefusedError:
            time.sleep(5)

    # Subscribe MQTT topic
    client.subscribe(topic)
    client.on_message = on_message

    # Start a thread to monitor message from publisher
    client.loop_forever()

    process_data(sensor_data)

if __name__ == '__main__':
    mqtt_subscriber()