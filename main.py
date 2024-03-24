from flask import Flask, send_file, url_for, render_template
from model import plot_predictions  
import matplotlib.pyplot as plt
import os
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def save_plot():
    plt.figure(figsize=(15, 7))
    plot_predictions() 
    plt.savefig('static/predictions.png')  # Save in static directory
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
    return send_file('static/predictions.png', mimetype='image/png')

if __name__ == '__main__':
    if not os.path.isfile('static/predictions.png'):
        save_plot()
    scheduler.start()  # Start the scheduler when running the app directly
    app.run(debug=True)
