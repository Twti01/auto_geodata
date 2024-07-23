import subprocess

# Pfad zur sensor_monitor.py
script_path = 'influx_gr6.py'

try:
    # Ausführung des Skripts
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)

    # Ausgabe und Fehler anzeigen
    print("Output:")
    print(result.stdout)
    print("Errors:")
    print(result.stderr)

except Exception as e:
    print(f"Fehler beim Ausführen des Skripts: {e}")
