from processing_calls import get_calls
from processing_occupancy import get_occupancy
from processing_weather import get_weather
import pandas as pd

def get_new_data():

    weather = get_weather()
    calls = get_calls()
    occupancy = get_occupancy()
    weather_calls= pd.merge(weather, calls, left_index=True, right_index=True, how='inner')
    weather_calls_occupancy= pd.merge(occupancy, weather_calls, left_index=True, right_index=True, how='inner')
    weather_calls_occupancy = weather_calls_occupancy[weather_calls_occupancy.index.year >= 2024]
    
    return weather_calls_occupancy

if __name__ == '__main__':
    x = get_new_data()
    print(x)