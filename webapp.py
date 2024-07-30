from flask import Flask, jsonify, request, abort
import influxdb, secrets, requests
from apikey import keys_list
import functools

app = Flask(__name__)

host = "172.16.231.188"
port = 8086
user = "linnart"
password = "linnart"
database = "abschluss_pi"

client = influxdb.InfluxDBClient(host=host, port=port, username=user, password=password)
client.switch_database(database)


def require_api_key(view_function):
    @functools.wraps(view_function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key in keys_list:
            return view_function(*args, **kwargs)
        else:
            abort(401)  # Unauthorized
    return decorated_function

@app.route("/bewegung", methods=['GET'])
@require_api_key
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
                             "gyro_x": point.get('gyro_x'),
                             "gyro_y": point.get('gyro_y'),
                             "gyro_z": point.get('gyro_z'),
                             "resulting_acceleration": point.get('resulting_acceleration'),
                             "resulting_angular_velocity": point.get('resulting_angular_velocity')
                             })
    return jsonify(measures), 200


@app.route("/position", methods=["GET"])
@require_api_key
def position():
    measures = []
    query = "SELECT * FROM koor"
    extract = client.query(query)
    points = extract.get_points(measurement="koor")
    if extract is not None:
        for point in points:
            measures.append({"lat": point.get('lat'),
                             "lon": point.get('lon')
                             })
    return jsonify(measures), 200

@app.route("/env", methods=["GET"])
@require_api_key
def env():
    measures = []
    query = "SELECT * FROM umwelt"
    extract = client.query(query)
    points = extract.get_points(measurement="umwelt")
    if extract is not None:
        for point in points:
            measures.append({"humid": point.get('humid'),
                             "temp": point.get('temp'),
                             "light": point.get('light')
                             })
    return jsonify(measures), 200

if __name__ == '__main__':
    app.run(host=host, port=5000, debug=True)