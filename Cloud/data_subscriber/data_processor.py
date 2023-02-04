import datetime
import pika
import json
import time

def process_data(sensor_data):
    count = 0
    outliers = []
    for data in sensor_data:
        data.append(datetime.datetime.fromtimestamp(int(data[0][:10])))
        if float(data[1]) > 50:
            outliers.append(data)
        count += 1
        #print("Timestamp: " + data[0] + ", Value: " + data[1], flush=True)

    for outlier in outliers:
        sensor_data.remove(outlier)

    if len(outliers) > 0:
        print("Outliers:", flush=True)
        for outlier in outliers:
            print("Timestamp: " + outlier[0] + ", Value: " + outlier[1], flush=True)
    else:
        print("No outliers were contained within the sensor data.", flush=True)

    calc_daily_avg(sensor_data)

def calc_daily_avg(sensor_data):
    daily_avg = []
    readings = 0
    avg = float(0)
    count = 0
    while count < len(sensor_data):
        avg += float(sensor_data[count][1])
        readings += 1
        if count == len(sensor_data) - 1:
            avg = avg / readings
            daily_avg.append(avg)
            print("Daily average for %d/%d/%d is %.2f" % 
                (sensor_data[count][2].day, sensor_data[count][2].month, 
                sensor_data[count][2].year, avg))
        elif sensor_data[count][2].day != sensor_data[count + 1][2].day:
            avg = avg / readings
            daily_avg.append(avg)
            print("Daily average for %d/%d/%d is %.2f" % 
                (sensor_data[count][2].day, sensor_data[count][2].month, 
                sensor_data[count][2].year, avg))
            readings = 0
            avg = 0

        count += 1

    publish_to_cloud(sensor_data, daily_avg)


def publish_to_cloud(sensor_data, daily_avg):
    rabbitmq_ip = "192.168.0.100"
    rabbitmq_port = 5672
    # Queue name
    rabbitmq_queque = "CSC8112"
    msg = "Hello!"

    # Connect to RabbitMQ service
    while True:
        try:
            print("Trying to connect", flush=True)
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port))
            break
        except pika.exceptions.AMQPConnectionError:
            time.sleep(5)
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue=rabbitmq_queque)

    # Produce message
    channel.basic_publish(exchange='', routing_key=rabbitmq_queque, body=json.dumps(msg))

    connection.close()
