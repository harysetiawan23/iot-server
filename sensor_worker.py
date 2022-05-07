import http
import time
import json
# import board
# import adafruit_dht
# import psutil
import iot_client
import http.client
import requests
from uuid import getnode as get_mac
mac = get_mac()

# # We first check if a libgpiod process is running. If yes, we kill it!
# for proc in psutil.process_iter():
#     if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
#         proc.kill()
# sensor = adafruit_dht.DHT11(board.D23)

def request_sensor_data():
    try:
        localhost = "http://127.0.0.1"
        node_red_port = "1880"
        path = "sensor"
        response = requests.get(url="{}:{}/{}".format(localhost,node_red_port,path))
        response = response.json()
        return response['temp'],response['humidity']
    except:
        pass

def sent_request_to_server(payload):
    try:
        server = "192.168.148.100"
        port = "3000"
        post_request = http.client.HTTPConnection(server,port=port)
        post_request.request("POST","/sensor",body=payload.encode("utf-8"))
        response = post_request.getresponse()
        print(response.read().decode())
    except:
        print("Unable to send data to server")


while True:
    try:
        try:
            # temp = sensor.temperature
            # humidity = sensor.humidity
            temp,humidity = request_sensor_data()
            sensordata = "<>".join([temp,humidity,str(mac)[:10]])
            print(sensordata)
        except:
            sensordata = "<>".join(["0","0",str(mac)[:10]])
        ## Send Sensor Data to Server
        encrypt_sensor_data = iot_client.encrypt_plaintext(sensordata)
        sent_request_to_server(encrypt_sensor_data)

        # print(encrypt_sensor_data)
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        # sensor.exit()
        raise error
    time.sleep(2.0)
