import paho.mqtt.client as mqtt
import string
import random
import buzzer

random_name = "".join(random.choices(string.ascii_letters + string.digits, k = 10))

client = mqtt.Client(client_id= random_name, clean_session=True)



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connection successful")
        client.subscribe("RPi/#")
    elif rc == 1:
        print("connection refused - incorrect protocol version")
    elif rc == 2:
        print("connection refused - invalid client")
    elif rc == 3:
        print("connection refused - server unavailable")
    elif rc == 4:
        print("connection refused - username or/and password incorrect")
    elif rc == 5:
        print("connection refused - not authorised")
    else:
        print(f"connection refused: {rc}")


def on_disconnect(client, userdata, rc):
    print(f"disconnected from server with result code: {rc}")


def on_message(client, userdata, message):
    print(f"{message.topic}: {message.payload.decode('utf-8')}")
    if message.topic == "RPi/GR6/buzzer/on": #or message.topic == "RPi/buzzer/on":
        buzzer.run()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect("mqtt-dashboard.com", 1883)
client.loop_forever()