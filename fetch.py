import json, requests
import zipfile

uri1 = "https://api.tfl.gov.uk/BikePoint/"
uri2 = "https://api.tfl.gov.uk/AirQuality/"
uri3 = "https://api.tfl.gov.uk/Road"
uri4 = "https://api.tfl.gov.uk/stationdata/tfl-stationdata-detailed.zip"

with open("api_key.json") as f:
    params = json.load(f)

try: 
    data1 = requests.get(uri1, params=params)
    data2 = requests.get(uri2, params=params)
    data3 = requests.get(uri3, params=params)
    data4 = requests.get(uri4, params=params)


    data1.raise_for_status()
    data2.raise_for_status()
    data3.raise_for_status()
    data4.raise_for_status()

    json_data1 = json.loads(data1.text)
    json_data2 = json.loads(data2.text)
    json_data3 = json.loads(data3.text)

    with open("bikepoints.json", "w") as f:
        json.dump(json_data1, f, indent=4)

    with open("airquality.json", "w") as f:
        json.dump(json_data2, f, indent=4)

    with open("roads.json", "w") as f:
        json.dump(json_data3, f, indent=4)

    with open("/opt/geodata/tfl-stations-data-detailed.zip", "wb") as f:
        for chunk in data4.iter_content(chunk_size=8192):
            f.write(chunk)

    with zipfile.ZipFile("/opt/geodata/tfl-stations-data-detailed.zip", "r") as zip_ref:
        zip_ref.extractall("/opt/geodata/station_data")

    print("Successfully updated data")

except Exception as e:
    print(e)
