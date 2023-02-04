import matplotlib.pyplot as plt
import datetime
import pandas as pd

from ml_engine import MLPredictor

def graph_data(sensor_data, avg_data):
    # Construct arrays
    x_data = []
    y_data = []
    for avg in avg_data:
        date_time = datetime.datetime.fromtimestamp(int(avg[0][:10]))
        x_data.append(date_time)
        y_data.append(float(avg[1]))

    # Plot graph
    plt.plot_date(x_data, y_data)

    plt.title("PM2.5 Sensor Value over Time")
    plt.xlabel("Date")
    plt.xticks(rotation=20)
    plt.ylabel("Value")
    plt.tight_layout()
    plt.show()
    plt.savefig("graph.png")

def machine_learning(sensor_data):
    df_input = []
    for data in sensor_data:
        date_time = datetime.datetime.fromtimestamp(int(data[0][:10]))
        df_input.append([date_time, data[1]])

    df = pd.DataFrame(df_input)
    df.columns = ["Timestamp", "Value"]

    predictor = MLPredictor(df)
    predictor.train()
    forecast = predictor.predict()

    fig = predictor.plot_result(forecast)
    fig.savefig("ml_graph.png")

def data_processor(sensor_data, avg_data):
    for avg in avg_data:
        date_time = datetime.datetime.fromtimestamp(int(avg[0][:10]))
        print("Daily average for %d/%d/%d is %.2f" % 
            (date_time.day, date_time.month, date_time.year, float(avg[1])), flush=True)

    for data in sensor_data:
        date_time = datetime.datetime.fromtimestamp(int(data[0][:10]))
        print("Time: %d:%d:%d, Date: %d/%d/%d, Value: %s" %
            (date_time.hour, date_time.minute, date_time.second, 
            date_time.day, date_time.month, date_time.year, data[1]), flush=True)

    graph_data(sensor_data, avg_data)
    machine_learning(sensor_data)