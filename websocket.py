from flask import Flask, render_template
import json, locale 
from datetime import datetime

app = Flask(__name__)


@app.route("/bikepoints")
@app.route("/bikepoints/<area>")
def bikepoints(area=None):

    with open("bikepoints.json", "r") as f:
        bike_file = json.load(f)

    data = []

    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")

    for bikepoint in bike_file:

        updated_time = bikepoint.get("additionalProperties")[0].get("modified", "Keine Angabe")

        iso_format = datetime.fromisoformat(updated_time.replace("Z", "+00:00"))
        updated_time = iso_format.strftime("%A, %d.%m.%Y %H:%M:%S")

        if area is None or area.lower() in bikepoint.get("commonName").lower():
            bikepoint_info = {
                "commonName": bikepoint.get("commonName") or "Keine Angabe",
                "lat": bikepoint.get("lat"),
                "lon": bikepoint.get("lon"),
                "updated_time": updated_time,
                "additionalProperties": []
            }
            for n in bikepoint.get("additionalProperties", []):
                properties = {
                    "key": n.get("key") or "Keine Angabe",
                    "value": n.get("value") or "Keine Angabe",
                }
                bikepoint_info["additionalProperties"].append(properties)

            if bikepoint_info["lat"] is None or bikepoint_info["lon"] is None:
                continue

            data.append(bikepoint_info)

         

    return render_template("index.html", bikepoint = data)



@app.route("/airquality")
def airquality():

    with open("airquality.json", "r") as f:
        air_file = json.load(f)
        
    airquality_data = {
        "UpdatedPeriod": air_file.get("updatePeriod") or "Keine Angabe",
        "Description": air_file.get("disclaimerText") or "Keine Angabe",
        "currentForecast": []}
    for n in air_file.get("currentForecast", []):
        infos = {
                "forecastType": n.get("forecastType") or "Keine Angabe",
                "Summary": n.get("forecastSummary") or "Keine Angabe", 
                "Nitrogen dioxide concentration": n.get("nO2Band") or "Keine Angabe",
                "Ozone concentration": n.get("o3Band") or "Keine Angabe",
                "Particulate matter(pm10)": n.get("pM10Band") or "Keine Angabe",
                "Particulate matter(pm25)": n.get("pM25Band") or "Keine Angabe",
                "Sulphur dioxide concentration": n.get("sO2Band") or "Keine Angabe",
                "Description": n.get("forecastText") or "Keine Angabe"
                }
        airquality_data["currentForecast"].append(infos)

    return render_template("airq.html", airquality = airquality_data)

@app.route("/road")
@app.route("/road/<q>")
def road(q=None):

    with open("roads.json", "r") as f:
        road_file = json.load(f)


    road_list = []

    for road in road_file:
        if q is None or q.lower() == road.get("displayName").lower():
            bounds = road.get("bounds")
            envelope = road.get("envelope")
            bounds = json.loads(bounds)
            envelope = json.loads(envelope)
            

            road_data = {
                    "road": road.get("displayName") or "Keine Angabe",
                    "traffic_state": road.get("statusSeverity") or "Keine Angabe",
                    "traffic_description": road.get("statusSeverityDescription") or "Keine Angabe",
                    "location": envelope                    
                    }
            road_list.append(road_data)

    return render_template("roads.html", road_list = road_list)


if __name__ == "__main__": 
    app.run(host="127.0.0.1", port=8000, debug=True)
