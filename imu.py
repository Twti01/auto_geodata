import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_imu_v2 import BrickIMUV2

# Konfiguration
HOST = "localhost"  # IP-Adresse des Brick Daemon
PORT = 4223
UID_IMU = "62fgA2"  # UID deines IMU Brick 2.0

class KalmanFilter:
    def __init__(self, process_noise=1e-5, measurement_noise=1e-2, error_covariance=1.0, initial_estimate=0.0):
        self.q = process_noise  # Prozessrauschen
        self.r = measurement_noise  # Messrauschen
        self.p = error_covariance  # Fehlerkovarianz
        self.x = initial_estimate  # Anfangsschätzung des Zustands
        self.k = 0  # Kalman-Gewinn

    def update(self, measurement):
        # Zeit-Update (Predict)
        self.p = self.p + self.q

        # Mess-Update (Correct)
        self.k = self.p / (self.p + self.r)
        self.x = self.x + self.k * (measurement - self.x)
        self.p = (1 - self.k) * self.p

        return self.x

# Initialisiere Kalman-Filter für Beschleunigungs- und Winkelgeschwindigkeitsdaten
kf_acc_x = KalmanFilter()
kf_acc_y = KalmanFilter()
kf_acc_z = KalmanFilter()
kf_gyro_x = KalmanFilter()
kf_gyro_y = KalmanFilter()
kf_gyro_z = KalmanFilter()

# Callback-Funktion für Beschleunigungsdaten
def cb_acceleration(x, y, z):
    filtered_x = kf_acc_x.update(x / 1000.0)
    filtered_y = kf_acc_y.update(y / 1000.0)
    filtered_z = kf_acc_z.update(z / 1000.0)
    print("Gefilterte Beschleunigung: x = {:.2f} m/s², y = {:.2f} m/s², z = {:.2f} m/s²".format(filtered_x, filtered_y, filtered_z))

# Callback-Funktion für Winkelgeschwindigkeitsdaten
def cb_angular_velocity(x, y, z):
    filtered_x = kf_gyro_x.update(x / 100.0)
    filtered_y = kf_gyro_y.update(y / 100.0)
    filtered_z = kf_gyro_z.update(z / 100.0)
    print("Gefilterte Winkelgeschwindigkeit: x = {:.2f} °/s, y = {:.2f} °/s, z = {:.2f} °/s".format(filtered_x, filtered_y, filtered_z))

if __name__ == "__main__":
    ipcon = IPConnection()  # Erzeuge IP-Verbindung
    imu = BrickIMUV2(UID_IMU, ipcon)  # Erzeuge Gerätobjekt

    try:
        ipcon.connect(HOST, PORT)  # Verbinde mit dem Brick Daemon
        time.sleep(2)  # Warte kurz, um sicherzustellen, dass die Verbindung stabil ist

        # Registriere Callback-Funktionen
        imu.register_callback(imu.CALLBACK_ACCELERATION, cb_acceleration)
        imu.register_callback(imu.CALLBACK_ANGULAR_VELOCITY, cb_angular_velocity)

        # Setze periodische Callback-Perioden auf 1 Sekunde (1000 ms)
        imu.set_acceleration_period(1000)
        imu.set_angular_velocity_period(1000)

        input("Drücke eine Taste, um das Programm zu beenden\n")  # Warte auf Benutzereingabe
    except Exception as e:
        print("Fehler:", e)
    finally:
        ipcon.disconnect()
