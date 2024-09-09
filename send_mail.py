import html
import smtplib
import json
import yaml
import copy
import subprocess
from datetime import datetime
from email.message import EmailMessage
from email.utils import formataddr


PORT = 587
EMAIL_SERVER = "smtp.gmail.com"
#Retrieve Receiver informations out of config-file

def load_file():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    return config

def save_file(config):
    with open("config.yaml", "w") as f:
        yaml.dump(config, f)


def load_json_files():

    with open("roads.json", "r") as f:
        road_file = json.load(f)

    with open("bikepoints.json", "r") as f:
        bike_file = json.load(f)

    with open("airquality.json", "r") as f:
        air_file = json.load(f)

    return road_file, bike_file, air_file


#Retrieve informations of subscriptions out of config-file(road_status, bike_status, weather_status)

#This function should get information to certain bikepoints and road_names and return bike_status and road_status, weather_status
def get_information(roads, bikepoints, weather_forecast):
    
    road_file, bike_file, air_file = load_json_files()

    road_status = []
    for road_name in roads:
        for road in road_file:
            if road.get("displayName").lower() == road_name.lower():
                status_severity = road.get("statusSeverity")
                status_description = road.get("statusSeverityDescription")
                road_status.append(f"Road: {road.get('displayName')} with status: {status_severity} and {status_description}.")
    

    bike_status = []

    for bikepoint in bikepoints:
        for bike in bike_file:
            if bike.get("commonName").lower().strip() == bikepoint.lower().strip():
                bike_counts = []
                for prop in bike.get("additionalProperties", []):

                    if prop.get("key") == "NbBikes":
                        bike_counts.append(prop.get("value"))
                    elif prop.get("key") == "NbStandardBikes":
                        bike_counts.append(prop.get("value"))
                    elif prop.get("key") == "NbEBikes":
                        bike_counts.append(prop.get("value"))

                bike_status.append(f"The bikepoint: {bike.get('commonName')} has a total amount of {bike_counts[0]} available bikes." 
                                 f" {bike_counts[1]} bikes count as standard bikes, while there are {bike_counts[2]} e-bikes.")

                break

    air_status = []

    for forecast in weather_forecast:
        print(f"Processing forecast: {forecast}")
        if forecast.lower() == "today":
            description = air_file["currentForecast"][0].get("forecastText")
            description = html.unescape(description)
            air_status.append(f"This is the forecast for today: {description}.")

        elif forecast.lower() == "tomorrow":
            description = air_file["currentForecast"][1].get("forecastText")
            description = html.unescape(description)
            air_status.append(f"This is the forecast for tomorrow: {description}.")

    print(f"air_status generated: {air_status}")

    return road_status, bike_status, air_status


def send_mail(subject, body, sender, receiver, password):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Automate Email", f"{sender}"))
    msg["To"] = receiver
    msg["BCC"] = sender
    msg.set_content(body, subtype="html")

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

#send mail for selected subscriptions at the beginning of each day and if status changes 
def send_daily_mail(sender, receiver, password):

    config = load_file()

    bikepoints = config.get("subscriptions", {}).get("bikepoints", [])

    roads = config.get("subscriptions", {}).get("roads", [])

    weather_forecast = config.get("subscriptions", {}).get("weather_forecast", [])

    date = datetime.now().strftime("%A, %d.%m.%Y. %H:%M:%S")

    subject = f"Daily Traffic and Weather Update for London on {date}"

    road_status, bike_status, air_status = get_information(roads, bikepoints, weather_forecast)

    body = f"""
            <html>
            <body>
                <h2>This is an automatic daily email to inform you about the london traffic state on {date}</h2>
                <p><strong>The weather_forecast is:</strong> {' '.join(air_status)}.</p> 
                <p>Road status for the Road names is as followed: {' '.join(road_status)}.</p>
                <p>These bikepoints have this amount of available bikes: {' '.join(bike_status)}</p>
            </body>
            </html>
            """

    send_mail(subject, body, sender, receiver, password)



def send_status_mail(sender, receiver, password, bike_areas=None, pollution=None, selected_roads=None):

    config = load_file()
    road_file, bike_file, air_file = load_json_files()
    unchanged_status = copy.deepcopy(config)

    print(f"bike_areas type: {type(bike_areas)}")
    print(f"pollution type: {type(pollution)}")
    print(f"selected_roads type: {type(selected_roads)}")

    if pollution:
        if isinstance(pollution, str):
            pollution = {pol: "unknown" for pol in pollution}
        config["selection"]["pollution"] = pollution
        print("changed pollution in config file.")

    if selected_roads:
        if isinstance(selected_roads, str):
            selected_roads = {road: "unknown" for road in selected_roads}
        config["selection"]["road_status"] = selected_roads
        print("changed roads in config file.")


    if bike_areas:
        if isinstance(bike_areas, str):
            bike_areas = {bike: "unknown" for bike in bike_areas}
        config["selection"]["ebikepoint"] = bike_areas
        print("changed bike_areas in config file.")

    save_file(config)

    #ensure if configuration exist if not create a key with empyt value
    airquality = config.get("selection", {}).get("pollution", {})
    road_status = config.get("selection", {}).get("road_status", {})
    bike_spots = config.get("selection", {}).get("ebikepoint", {})


    for road, value in road_status.items():
        for n in road_file:
            if road.lower().strip() == n.get("displayName").lower().strip():

                single_road_status = (value or "unknown").lower()
                status = n.get("statusSeverity", "").lower()
                
                if road.lower() not in road_status:
                    road_status[road] = status                    
                    print("changed road_status")

                if status != single_road_status:
                    print("Statusänderung und damit Bereitschaft Email zu versenden")
                    road_status[road] = status


    config["selection"]["road_status"] = road_status
    save_file(config)


    forecast_today = air_file["currentForecast"][0]

    for pollutant, value in airquality.items():

        formated_pollutant = pollutant[0].lower() + pollutant[1:].capitalize() 
        forecast_key = f"{formated_pollutant}Band"
        forecast_value = forecast_today.get(forecast_key, "").lower()
        print(forecast_key)
        value_lowered = (value or "unknown").lower()

        if pollutant.lower() == forecast_key[:-4].lower() and value_lowered != forecast_value:
                print("Statusänderung bei der Luftverschmutzung")
                airquality[pollutant]= forecast_value

                save_file(config)

    
    for area, ebikes in bike_spots.items(): 
        area = str(area)
        ebikes = ebikes or 0
        for bikepoint in bike_file:
            if area.lower() in bikepoint.get("commonName").lower():
               for n in bikepoint.get("additionalProperties"):
                   if n.get("key") == "NbEBikes":
                       ebike_count = int(n.get("value"))
    
                       if ebike_count > ebikes:
                            print("Statusänderung bei der Anzahl an Ebikes.")
                            bike_spots[area] = ebike_count

                            save_file(config)


    current_status = config

    if unchanged_status != current_status:
        save_file(config)
        #Email verschicken!

        date = datetime.now().strftime("%A, %H:%M:%S")

        subject = f"Status mail to inform you about the newest changes in londons traffic state"

        body = f"""
                <html>
                <body>
                    <h2>Here are the newest status changes in the london traffic state on {date}</h2>
                    <p>The following pollutants are predicted: {config['selection']['pollution']}</p>
                    <p>Road status for the Road names is as followed: {config['selection']['road_status']}.</p>
                    <p>These bikepoints have this amount of available e-bikes: {config['selection']['ebikepoint']}</p>
                </body>
                </html>
                """


        print("email sollte verschickt werden")

        send_mail(subject, body, sender, receiver, password)





def email_time(time="08:00"):
    hours, minutes = time.split(":")
    cron = f"{minutes} {hours} * * * /home/user/.venv/bin/python3 /opt/geodata/subscribe.py Dailymail --send"

    output = subprocess.getoutput("crontab -l")

    # Entfernen Sie alte 'Dailymail'-Einträge und fügen Sie den neuen hinzu
    update = "\n".join([line for line in output.splitlines() if "Dailymail" not in line])
    update += f"\n{cron}\n"

    command = f"(echo '{update}') | crontab -"
    subprocess.run(command, shell=True, check=True)
    print(f"Crontab updated: Daily mail scheduled at {time}")

    #selection by config file z.B. (e-bike counts in region under 5, road_status: if serious, if high amount of pollution)
    
    
#snippets
    #deleteable_roads = [road for road in road_status if road not in roads]

    #for road in deleteable_roads:
    #    del config["selection"]["road_status"][road]

                #single_road_status = config["selection"]["road_status"].get(road, "").lower()
