from flask import Flask, send_file
from model import plot_predictions  
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world!' 

@app.route('/predictions')
def predictions():
    plt.figure(figsize=(15, 7))
    plot_predictions() 
    plt.savefig('predictions.png')
    plt.close()
    
    # Return the plot image file in the response
    return send_file('predictions.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

