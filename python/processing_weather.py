import pandas as pd
from io import StringIO
import requests

csv_url = 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=51459&Year=2023&Month=3&Day=1&time=&timeframe=2&submit=Download+Data'

response = requests.get(csv_url)

# Check if the request was successful
if response.ok:
    # Use StringIO to convert the text data into a file-like object so that pandas can read it
    data = StringIO(response.text)
    
    # Read the data into a pandas DataFrame
    weather = pd.read_csv(data)
    
    weather = weather.rename(columns={'Date/Time': 'Date', 'Min Temp (°C)': 'min_temp_cels', 'Total Precip (mm)': 'total_precip_mm'})

    weather['Date'] = pd.to_datetime(weather['Date']) 
    weather.set_index('Date', inplace=True)

    weather = weather[['min_temp_cels', 'total_precip_mm']]
    weather['min_temp_cels'] = weather['min_temp_cels'].interpolate(method='linear')
    weather['total_precip_mm'] = weather['total_precip_mm'].interpolate(method='linear')

else:
    print(f'Failed to retrieve data. Status code: {response.status_code}')