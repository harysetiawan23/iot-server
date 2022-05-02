from flask import Flask,request

app = Flask(__name__)

@app.route('/',methods=['POST'])
def hello_world():
    if request.method == 'POST':
        return {"message":"Post Hello World!"}
    return {"message":"Hello World!"}

if __name__ == '__main__':
    app.run()