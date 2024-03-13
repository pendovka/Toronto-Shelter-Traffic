import pandas as pd
from io import StringIO
import requests

# REFRESHED DAILY

csv_urls = {
    '2023': 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=51459&Year=2023&Month=3&Day=1&time=&timeframe=2&submit=Download+Data',
    '2022': 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=51459&Year=2022&Month=3&Day=1&time=&timeframe=2&submit=Download+Data',
    '2021': 'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=51459&Year=2021&Month=3&Day=1&time=&timeframe=2&submit=Download+Data'
}

weather_data_frames = []

for year, url in csv_urls.items():
    response = requests.get(url)
    if response.ok:
        data = StringIO(response.text)
        weather_df = pd.read_csv(data)
        weather_df = weather_df.rename(columns={
            'Date/Time': 'Date',
            'Min Temp (°C)': 'min_temp_cels'
        })
        weather_df['Date'] = pd.to_datetime(weather_df['Date'])
        weather_df.set_index('Date', inplace=True)
        weather_df = weather_df[['min_temp_cels']]
        weather_df['min_temp_cels'] = weather_df['min_temp_cels'].interpolate(method='linear')
        
        weather_data_frames.append(weather_df)
    else:
        print(f'Failed to retrieve data for {year}. Status code: {response.status_code}')

concatenated_weather = pd.concat(weather_data_frames)
concatenated_weather.sort_index(ascending=True, inplace=True)

print(concatenated_weather)
