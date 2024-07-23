from flask import Flask, request, jsonify
import sqlite3


app = Flask('MyLoc')


def execute(sql):
    conn = sqlite3.connect("myloc.sqlite")
    try:
        result = conn.execute(sql)
        conn.commit()
        return result
    except sqlite3.Error as err:
        print(err)
        return None
    
execute("CREATE TABLE IF NOT EXISTS loc (id INTEGER PRIMARY KEY NOT NULL, ts TEXT NOT NULL, name TEXT, latitude REAL NOT NULL, longitude REAL NOT NULL)")

@app.route("/myloc", methods = ['GET'])
@app.route("/myloc/<q>", methods = ['GET'])
def loc_get(q = None):
    loc_list = []
    if q is None:
        result = execute("SELECT * FROM loc")
    else:
        result = execute("SELECT * FROM loc WHERE {q}")
    if result is not None:
        for row in result:
            loc_list.append({
                "name": row[2],
                "ts": row[1],
                "latitude": row[3],
                "longitude": row[4]
            })
    return jsonify(loc_list), 200

@app.route("/myloc", methods=['POST'])
def loc_post():
    data_json = request.get_json()
    print(data_json)
    sql = f"INSERT INTO loc (ts, name, latitude, longitude) VALUES ('{request.form.get('ts')}','{request.form.get('name')}', {request.form.get('latitude')}, {request.form.get('longitude')})"
    print(sql)
    result = execute(sql)
    if result is None:
        return "DB ERROR!", 500
    else:
        return "OK", 200

@app.route("/myloc/<id>", methods=["DELETE"])
def loc_delete(id):
    sql = f"DELETE FROM loc WHERE id = {id}"
    result = execute(sql)
    if result is None:
        return "DB ERROR!", 500
    else:
        return "DONE", 200

if __name__ == "__main__":
    app.run(host="192.168.178.101", port=5000, debug=True)