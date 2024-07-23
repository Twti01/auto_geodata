import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_gps_v3 import BrickletGPSV3

# Konfiguration
HOST = "localhost"
PORT = 4223
UID_GPS = "21LD"  # Ändere XYZ zur UID deines GPS Bricklet 3.0

# Callback-Funktion für GPS-Daten
def cb_coordinates(latitude, ns, longitude, ew):
    print("Latitude: {:.3f} {}".format(latitude / 1000000.0, ns))
    print("Longitude: {:.3f} {}".format(longitude / 1000000.0, ew))
    print("")

if __name__ == "__main__":
    ipcon = IPConnection()  # Erzeuge IP-Verbindung
    gps = BrickletGPSV3(UID_GPS, ipcon)  # Erzeuge Gerätobjekt

    try:
        ipcon.connect(HOST, PORT)  # Verbinde mit dem Brick Daemon
        # Warte eine kurze Zeit, um sicherzustellen, dass die Verbindung stabil ist
        time.sleep(2)

        # Registriere Callback für GPS-Daten
        gps.register_callback(gps.CALLBACK_COORDINATES, cb_coordinates)
        # Setze periodische Callback-Periode auf 1 Sekunde (1000 ms)
        gps.set_coordinates_callback_period(1000)

        input("Drücke eine Taste, um das Programm zu beenden\n")  # Warte auf Benutzereingabe
    except Exception as e:
        print("Fehler:", e)
    finally:
        ipcon.disconnect()