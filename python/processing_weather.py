import requests
from datetime import datetime
import json
import os
import pandas as pd

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.35&daily=temperature_2m_min&timezone=America%2FNew_York&past_days=92"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        dataframe = {'Date': data['daily']['time'], 'temperature': data['daily']['temperature_2m_min']}
        dataframe = pd.DataFrame(dataframe)
        dataframe['Date'] = pd.to_datetime(dataframe['Date'])
        dataframe.set_index('Date', inplace=True)
        return dataframe
    else:
        print("Failed to retrieve data:", response.status_code)
        return None



