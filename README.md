# CSC8112-Internet-of-Things
## Overview
This project makes use of data from Newcastle Universities Urban Observatory.
The main goal of this project was to develop a data pipeline from an edge device (sensor) to the cloud.

**Edge Device 1 --> EMQX --> Edge Device 2 --> RabbitMQ --> Cloud**

## Task 1
The first task involved first getting the data from the Urban Observatory via a HTTP GET request.
This retrieved far more data than was needed so it was filtered to just the data for the PM2.5 sensor.
A data injector application was then developed, this uses EMQX to publish the sensor data one value at a time in order to mimic a stream of data.
This data injector application is running as a Docker image.
The data published to EMQX is subscribed to by a subscriber running as a separate Docker image.
## Task 2
This task involved using the data that had been received from the EMQX service.
One issue I had was that the EMQX subscriber would not be able to keep up so would lose some messages.
This was solved by adding a small delay of only 0.001 seconds between each message.
This resulted in zero of 8,000 messages being lost when before it was 20-40 that were being lost each time and only added an 8 second delay.
This received data was then processed to remove outliers.
The final part of task two was to send this data to a RabbitMQ message broker.
## Task 3
The first part of this task was to subscribe to data from the RabbitMQ message broker.
This data was then used to produce a graph and a machine learning engine was used to predict future values of this sensor and then produce a graph of this data.
