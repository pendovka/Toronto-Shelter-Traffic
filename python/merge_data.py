from processing_calls import calls
from processing_occupancy import occupancy
from processing_weather import weather
import pandas as pd

weather_calls= pd.merge(calls, weather, left_index=True, right_index=True, how='inner')
weather_calls_occupancy= pd.merge(occupancy, weather_calls, left_index=True, right_index=True, how='inner')

print(weather_calls_occupancy)