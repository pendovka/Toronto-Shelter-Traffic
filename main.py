from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world!' 

@app.route('/seva')
def get_seva():
    return 'seva'

if __name__ == '__main__':
    app.run(debug=True)
