from flask import Flask, send_file, url_for, render_template
from model import plot_predictions  
import matplotlib.pyplot as plt
import os
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

i = 0
b=0

@app.route('/')
def index():

    i +=  1

    return str(i)

