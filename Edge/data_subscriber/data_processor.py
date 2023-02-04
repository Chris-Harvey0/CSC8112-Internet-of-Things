import datetime
import pika
import json
import time

from rabbitmq_publisher import rabbitmq_publisher

def process_data(sensor_data):
    outliers = []
    # Find outliers
    for data in sensor_data:
        if float(data[1]) > 50:
            outliers.append(data)
        #print("Timestamp: " + data[0] + ", Value: " + data[1], flush=True)

    for outlier in outliers:
        sensor_data.remove(outlier)

    # Print outliers
    if len(outliers) > 0:
        print("Outliers:", flush=True)
        for outlier in outliers:
            print("Timestamp: " + outlier[0] + ", Value: " + outlier[1], flush=True)
    else:
        print("No outliers were contained within the sensor data.", flush=True)

    calc_avg_data(sensor_data)

def calc_avg_data(sensor_data):
    avg_data = []
    readings_in_day = 0
    avg = float(0)
    count = 0

    while count < len(sensor_data):
        date_time = datetime.datetime.fromtimestamp(int(sensor_data[count][0][:10]))
        avg += float(sensor_data[count][1])
        readings_in_day += 1

        # If last value in array
        if count == len(sensor_data) - 1:
            avg = avg / readings_in_day
            avg_data.append([sensor_data[count][0], avg])
            print("Daily average for %d/%d/%d is %.2f" % 
                (date_time.day, date_time.month, date_time.year, avg), flush=True)

        else:
            next_value_date_time = datetime.datetime.fromtimestamp(int(sensor_data[count+1][0][:10]))
            # Calc average for the day
            if date_time.day != next_value_date_time.day:
                avg = avg / readings_in_day
                avg_data.append([sensor_data[count][0], avg])

                print("Daily average for %d/%d/%d is %.2f" % 
                    (date_time.day, date_time.month, date_time.year, avg), flush=True)
                readings_in_day = 0
                avg = 0

        count += 1

    rabbitmq_publisher(sensor_data, avg_data)
