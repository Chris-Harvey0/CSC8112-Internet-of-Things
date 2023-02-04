import pika
import time
import json

def rabbitmq_publisher(sensor_data, avg_data):
    rabbitmq_ip = "192.168.0.100"
    rabbitmq_port = 5672
    # Queue name
    rabbitmq_queque = "CSC8112"

    # Connect to RabbitMQ service
    while True:
        try:
            print("Trying to connect to RabbitMQ", flush=True)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port))
            break
        except pika.exceptions.AMQPConnectionError:
            time.sleep(5)
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=rabbitmq_queque)

    # Publish sensor data
    for data in sensor_data:
        msg = str(data[0]) + "," + str(data[1])
        channel.basic_publish(exchange='', routing_key=rabbitmq_queque, body=json.dumps(msg))
    channel.basic_publish(exchange='', routing_key=rabbitmq_queque, body=json.dumps("end of sensor data"))

    # Publish average data
    for avg in avg_data:
        msg = str(avg[0]) + "," + str(avg[1])
        channel.basic_publish(exchange='', routing_key=rabbitmq_queque, body=json.dumps(msg))
    channel.basic_publish(exchange='', routing_key=rabbitmq_queque, body=json.dumps("end"))

    connection.close()