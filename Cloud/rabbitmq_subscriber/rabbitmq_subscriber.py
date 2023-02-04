import json
import pika
import time
from data_processor import data_processor

msg_data = []

def callback(ch, method, properties, body):
    data = json.loads(body)
        
    if data != "end":
        msg_data.append(data)
    else:
        ch.close()

        sensor_data = []
        avg_data = []
        switch_array = False

        # Construct sensor and avg arrays
        for data in msg_data:
            if data != "end of sensor data":
                split_data = data.split(",")
                if switch_array == False:
                    sensor_data.append(split_data)
                else:
                    avg_data.append(split_data)
            else:
                switch_array = True

        data_processor(sensor_data, avg_data)

def rabbitmq_subscriber():
    rabbitmq_ip = "192.168.0.100"
    rabbitmq_port = 5672
    # Queue name
    rabbitmq_queque = "CSC8112"

    # Connect to RabbitMQ service with timeout 1min
    while True:
        try:
            print("Trying to connect to RabbitMQ", flush=True)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, socket_timeout=60))
            break
        except pika.exceptions.AMQPConnectionError:
            time.sleep(5)
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=rabbitmq_queque)
    channel.basic_consume(queue=rabbitmq_queque, auto_ack=True, on_message_callback=callback)
    channel.start_consuming()

if __name__ == '__main__':
    rabbitmq_subscriber()
