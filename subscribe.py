import argparse
import yaml
from getpass import getpass
from send_mail import send_daily_mail, send_status_mail, email_time

file = "config.yaml"

def open_file():
    with open(file, "r") as f:
        config = yaml.safe_load(f) or {}

    return config

def save_file(config):
    with open(file, "w") as f:
        yaml.dump(config, f)

def login():

    config = open_file()

    email_section = config.get("email", {})

    if "receiver" in email_section and "password" in email_section:
        print("Already logged in. Please log out before logging in again.")

    else: 
        email_address = input("Enter your email address: ")
        password_input = getpass("Enter your password: ")

        if "email" not in config:
            config["email"] = {}

        config["email"]["receiver"] = email_address
        config["email"]["password"] = password_input

        save_file(config)

        print("Successfully logged in.")



def logout():

    config = open_file()

    if "receiver" in config["email"] or "password" in config["email"]:
        del config["email"]["receiver"]
        del config["email"]["password"]

        save_file(config)

        print("Successfully logged out.")

    else:
        print("Not logged in, so could not log out")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Subscribe to Newsletter.")
    parser.add_argument("action", choices=["login", "logout", "Dailymail", "Statusmail"])
    parser.add_argument("-t", "--time", default="08:00", help="Sets the time for the Dailymail in format: (HH:MM)")
    parser.add_argument("-s", "--send", action="store_true", help="Sending daily mail")
    parser.add_argument("--bikepoints", nargs="*", type=str, help="Comma-separated list of bikepoints")
    parser.add_argument("--pollutants", nargs="*", type=str, help="Comma-separated list of pollutants")
    parser.add_argument("--roads", nargs="*", type=str, help="Comma-separated list of road names")
    args = parser.parse_args()

    config = open_file()
    email_section = config.get("email", {})
    sender = email_section.get("sender")
    receiver = email_section.get("receiver")
    password = email_section.get("password")

    if args.action == "login":
        login()

    elif args.action == "logout":
        logout()
        
    elif args.action == "Dailymail":
        if args.send:
            send_daily_mail(sender=sender, receiver=receiver, password=password)
        else:
            email_time(time=args.time)

    elif args.action == "Statusmail":
        bike_areas = {bike: "unknown" for bike in args.bikepoints} if args.bikepoints else None
        pollution = {pol: "unknown" for pol in args.pollutants} if args.pollutants else None
        selected_roads = {road: "unknown" for road in args.roads} if args.roads else None
        send_status_mail(sender=sender, receiver=receiver, password=password, bike_areas=bike_areas, pollution=pollution, selected_roads=selected_roads)

