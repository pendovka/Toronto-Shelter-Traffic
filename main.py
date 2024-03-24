from flask import Flask, send_file, url_for, render_template
from model import plot_predictions  
import matplotlib.pyplot as plt
import os
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def save_plot():
    plt.figure(figsize=(15, 7))
    plot_predictions() 
    plt.savefig('predictions.png')
    plt.close()

# Initialize the scheduler with your preferred settings.
scheduler = BackgroundScheduler()
scheduler.add_job(func=save_plot, trigger="interval", hours=1)
scheduler.start()

@app.route('/')
def index():
    # Provide a link to the predictions plot or embed it in an HTML page.
    return render_template('index.html', plot_url=url_for('predictions'))

@app.route('/predictions')
def predictions():
    # Return the plot image file in the response
    return send_file('predictions.png', mimetype='image/png')

if __name__ == '__main__':
    # Make sure 'predictions.png' exists before the first request
    if not os.path.isfile('predictions.png'):
        save_plot()
    app.run(debug=True)
