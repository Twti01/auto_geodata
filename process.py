import pandas as pd 
import argparse 
import numpy as np

df_stations = pd.read_csv("station_data/Stations.csv")
df_stationpoints = pd.read_csv("station_data/StationPoints.csv")
df_toilets = pd.read_csv("station_data/Toilets.csv")
df_ramproute = pd.read_csv("station_data/RampRoutes.csv")
df_lift = pd.read_csv("station_data/Lifts.csv")
df_interchange = pd.read_csv("station_data/StepFreeIntechangeInfo.csv")


def station_info(station, wifi=False, location=True, baby_change=False, bus_interchange=False, ramp_route=False, lift=False, Interchange_info=False):

    if station not in df_stations["Name"].values:
        print("This is not a valid station name. Please check if the spelling is right!")


    station_name = df_stations[df_stations["Name"] == station].iloc[0]
    station_id = station_name["UniqueId"]

    if wifi:
        wifi_pos = df_stations[df_stations["UniqueId"] == station_id]
        if not wifi_pos.empty:
            wifi_info = wifi_pos.iloc[0]["Wifi"]
            if pd.notna(wifi_info) and wifi_info == True:
                print("Wifi Availability: yes")
            else:
                print("No Wifi Option")
        else:
            print("Did not match any corresponding station id.")

    if location:
        location_pos = df_stationpoints[df_stationpoints["StationUniqueId"] == station_id]
        if not location_pos.empty:
            mean_lat = np.mean(location_pos["Lat"])
            mean_lon = np.mean(location_pos["Lon"])
            if mean_lat and mean_lon:
                print(f"Location: Lat: {mean_lat:.3f}, Lon: {mean_lon:.3f}")
            else:
                print("No location entry.")
        else:
            print("Did not match any corresponding station id.")

    if baby_change:
        baby_change_pos = df_toilets[df_toilets["StationUniqueId"] == station_id]
        if not baby_change_pos.empty:
            if baby_change_pos["HasBabyChanging"].any() == True:
                print(f"Baby Changing Facility: Yes, this station has a Baby Changing Facility.")
            else:
                print("Baby Changing Facility: No Changing Facility at this station.")
        else:
            print("Did not match any corresponding station id.")


    if bus_interchange:
        bus_interchange_pos = df_stations[df_stations["UniqueId"] == station_id]
        if not bus_interchange_pos.empty:
            bus_interchange_value = bus_interchange_pos.iloc[0]["MainBusInterchange"]
            if not pd.notna(bus_interchange_value) and bus_interchange_value == True:
                print(f"Bus Interchange: {bus_interchange_value}")
            else:
                print("No Bus Interchange.")
        else:
            print("Did not match any corresponding station id.")

    if ramp_route:
        ramp_route_pos = df_ramproute[(df_ramproute["From"].str.contains(station_id)) | (df_ramproute["To"].str.contains(station_id))]
        if not ramp_route_pos.empty:
            print("These are possible ramp routes:")
            for _, row in ramp_route_pos.iterrows():
                print(f"From {row['From']} to {row['To']}.")
        else:
            print("Did not match any corresponding station id.")

    if lift:
        lift_pos = df_lift[df_lift["StationUniqueId"] == station_id]
        if not lift_pos.empty:
            lift_value = lift_pos["FromAreas"]
            if not lift_value.empty:
                print(f"Lift Availability: {lift_value}")
            else:
                print("No Lift information available.")
        else:
            print("Did not match any corresponding station id.")

    if Interchange_info:
        interchange_pos = df_interchange[(df_interchange["FromPlatformUniqueId"].str.contains(station_id)) | (df_interchange["ToPlatformUniqueId"].str.contains(station_id))]
        if not interchange_pos.empty:
            print("These are possible interchanges:")
            for _, row in interchange_pos.iterrows():
                print(f"From {row['FromPlatformUniqueId']} to {row['ToPlatformUniqueId']} within a distance of {row['DistanceInMetres']} metres.")
        else:
            print("Did not match any corresponding station id.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="StationInfo", description="Retrieve Information about stations in London.", epilog="Have Fun!")

    parser.add_argument("station", help="Neccessary Input of station name.")
    parser.add_argument("-w","--wifi", action="store_true", help="Show Wifi Availability")
    parser.add_argument("-lo","--location", action="store_true", help="Retrieve Location of station")
    parser.add_argument("-ba","--babychange", action="store_true", help="Lists possible babychange locations")
    parser.add_argument("-bu","--businterchange", action="store_true", help="Lists possible businterchange locations")
    parser.add_argument("-r","--ramproute", action="store_true", help="Shows Ramproutes Availability")
    parser.add_argument("-li","--lift", action="store_true", help="Retrieves Lift informations.")
    parser.add_argument("-i", "--interchange", action="store_true", help="Shows all interchange possiblities.")

    args = parser.parse_args()
    
    station_info(args.station, args.wifi, args.location, args.babychange, args.businterchange, args.ramproute, args.lift, args.interchange)

