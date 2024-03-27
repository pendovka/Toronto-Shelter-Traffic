from flask import Flask

app = Flask(__name__)

i = 0
b = 0

@app.route('/')
def index():

    i +=  1

    return str(i)

