import sqlite3
import datetime
import random

conn = sqlite3.connect("example.sqlite")
print("connection to db")

sql = "CREATE TABLE IF NOT EXISTS dht11 (id INTEGER PRIMARY KEY NOT NULL,  timestamp TEXT NOT NULL, temp REAL NOT NULL, humid REAL NOT NULL)"


try:
    conn.execute(sql)
    conn.commit()
    print("table created!")
except sqlite3.Error as err:
    print(err)

def insert():
    for i in range (100):
        ts = datetime.datetime.strptime("2024-06-05 16:00:00", "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1)
        temp = 25.0 + random.random()
        humid = 55.0 + random.random()
        sql = f"INSERT INTO dht11 (timestamp, temp, humid) VALUES ('{ts.strftime('%Y-%m-%d %H:%M:%S')}', {temp: .3f}, {humid: .3f})"
        try:
            conn.execute(sql)
        except sqlite3.Error as err:
            print(err)
    conn.commit()

def select():
    sql = "SELECT id, timestamp, temp, humid FROM dht11 WHERE id <= 10"
    try:
        cursor = conn.execute(sql)
    except sqlite3.Error as err:
        print(err)

    for row in cursor:
        print(row)

sql = "UPDATE dht11 SET temp = 30.0 WHERE id = 1"
try:
    conn.execute(sql)
    conn.commit()
except sqlite3.Error as err:
    print(err)

sql = "DELETE FROM dht11 WHERE temp = 30.0"
sql = "DROP TABLE dht11"

print("table updated")