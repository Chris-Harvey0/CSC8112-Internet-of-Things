import json
import time
import requests
from paho.mqtt import client as mqtt_client


def get_sensor_data():
    # Target URL
    url = "http://uoweb3.ncl.ac.uk/api/v1.1/sensors/PER_AIRMON_MONITOR1135100/" \
          "data/json/?starttime=20220601&endtime=20220831"

    # Request data from Urban Observatory Platform
    resp = requests.get(url)

    # Convert response(Json) to dictionary format
    raw_data_dict = resp.json()

    #print(raw_data_dict, flush=True)

    # Extract PM2.5 sensor data
    sensor_data = raw_data_dict["sensors"][0]["data"]["PM2.5"]

    # Construct output data
    output_data = []
    for data in sensor_data:
        sensor_timestamp = data["Timestamp"]
        sensor_value = data["Value"]
        output_data.append(str(sensor_timestamp) + "," + str(sensor_value))

    return output_data

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT OK!", flush=True)
    else:
        print("Failed to connect, return code %d\n", rc, flush=True)

def mqtt_publisher(sensor_data):
    mqtt_ip = "mqtt-broker"
    mqtt_port = 1883
    topic = "CSC8112"

    # Create a mqtt client object
    client = mqtt_client.Client()

    # Connect to MQTT service
    client.on_connect = on_connect
    while True:
        try:
            print("Trying to connect to MQTT", flush=True)
            client.connect(mqtt_ip, mqtt_port)
            break
        except ConnectionRefusedError:
            time.sleep(5)

    # Publish message to MQTT
    for data in sensor_data:
        msg = json.dumps(data)
        client.publish(topic, msg)
        time.sleep(0.001)

    # End of transmission
    client.publish(topic, json.dumps("end"))
    client.disconnect()

if __name__ == '__main__':
    output_data = get_sensor_data()
    mqtt_publisher(output_data)
