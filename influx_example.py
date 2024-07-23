import influxdb
import datetime
import random
import time
import threading

db = influxdb.InfluxDBClient(host="127.0.0.1", port=8086, username="linnart", password="linnart")

print("connection to influxdb done!")

db.switch_database("db_damm")

print("DB aktiv")

def worker(sensor_name, sensor_type, temp, humid, interval):
    while True:
        data = {
            "measurement": "env",
            "time": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tags": {
                "owner": "linnart",
                "name": sensor_name,
                "type": sensor_type,
            },
            "fields": {
                "temp": temp + round(random.random(), 2),
                "humid": humid + round(random.random(), 2)
            }
        }
        print(data)
        if not db.write_points([data]):
            print("error write points!")
        time.sleep(interval)

threading.Thread(target=worker, args=("S1", "DHT-11", 20.0, 45.0, 5)).start()
threading.Thread(target=worker, args=("S2", "DHT-11", 22.0, 50.0, 10)).start()