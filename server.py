import json
from flask import Flask,request

app = Flask(__name__)

import iot_server

@app.route('/sensor',methods=['POST'])
def hello_world():
    if request.method == 'POST':
        payload = request.data.decode()
        # print(payload)

        decrypted_payload = iot_server.decyrpt_payload(payload)
        decrypted_payload = decrypted_payload.split("<>")
        return {"message":decrypted_payload}
    return {"message":"Hello World!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000)