from flask import Flask, jsonify, request, abort
import influxdb, secrets, requests

app = Flask(__name__)

host = "172.16.231.188"
port = 8086
user = "linnart"
password = "linnart"
database = "db_damm"

client = influxdb.InfluxDBClient(host=host, port=port, username=user, password=password)
client.switch_database(database)

def gen_api_keys(number, key_len=16):
    keys = []
    for i in range(number):
        key = secrets.token_hex(key_len)  
        keys.append(key)
    return keys

keys_list = gen_api_keys(15)

def require_api_key(view_function):
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key in keys_list:
            return view_function(*args, **kwargs)
        else:
            abort(401)  # Unauthorized
    return decorated_function

@app.route("/bewegung", methods=['GET'])
def movement():
    measures = []
    query = "SELECT * FROM bewegung"
    extract = client.query(query)
    points = extract.get_points(measurement="bewegung")
    if extract is not None:
        for point in points:
            measures.append({"time": point.get('time'),
                             "acc_x": point.get('acc_x'),
                             "acc_y": point.get('acc_y'),
                             "acc_z": point.get('acc_z'),
                             "gyro_x": point.get('gyro_x')
                             })
    return jsonify(measures), 200

if __name__ == '__main__':
    app.run(host=host, port=5000, debug=True)