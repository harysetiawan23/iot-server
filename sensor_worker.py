import http
import time
import json
# import board
# import adafruit_dht
# import psutil
import iot_client
import http.client


# # We first check if a libgpiod process is running. If yes, we kill it!
# for proc in psutil.process_iter():
#     if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
#         proc.kill()
# sensor = adafruit_dht.DHT11(board.D23)

def sent_request_to_server(payload):
    server = "127.0.0.1"
    port = "3000"
    post_request = http.client.HTTPConnection(server,port=port)
    post_request.request("POST","/sensor",body=payload.encode("utf-8"))
    response = post_request.getresponse()
    print(response.read().decode())


while True:
    try:
        # temp = sensor.temperature
        # humidity = sensor.humidity
        temp = str(77)
        humidity = str(88)
        sensordata = "<>".join([temp,humidity])

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