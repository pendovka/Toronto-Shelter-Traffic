from extraction import fetch_data
import pandas as pd 
import numpy as np

# REFRESHED DAILY

def get_occupancy():

    package_id_occupancy = "daily-shelter-overnight-service-occupancy-capacity"

    occupancy2024 = fetch_data(package_id_occupancy, 0)

    occupancy2024['OCCUPANCY_DATE'] = pd.to_datetime(occupancy2024['OCCUPANCY_DATE'])

    occupancy2024['OCCUPANCY_DATE'] = pd.to_datetime(occupancy2024['OCCUPANCY_DATE'])

    occupancy2024.sort_values(by='OCCUPANCY_DATE', inplace=True)
    occupancy2024.set_index('OCCUPANCY_DATE', inplace=True)
    occupancy2024 = occupancy2024.rename_axis('Date')

    occupancy2024.fillna(0, inplace=True)

    occupancy2024['occupancy_rate'] = occupancy2024['OCCUPANCY_RATE_BEDS'] + occupancy2024['OCCUPANCY_RATE_ROOMS']

    daily_mean_occupancy_rate = occupancy2024['occupancy_rate'].resample('D').mean()
    occupancy2024 = daily_mean_occupancy_rate.to_frame(name='occupancy_rate')

    occupancy2024['occupancy_rate_lag_day'] = occupancy2024['occupancy_rate'].shift(1)
    occupancy2024['occupancy_rate_lag_day'] = occupancy2024['occupancy_rate_lag_day'].ffill()
    occupancy2024['occupancy_rate_lag_day'] = occupancy2024['occupancy_rate_lag_day'].bfill()

    occupancy2024['occupancy_rate_lag_day'] = np.log(occupancy2024['occupancy_rate_lag_day']).round(2)

    occupancy = occupancy2024.drop(columns  = ['occupancy_rate'])
    
    return occupancy

if __name__ == '__main__':
    x = get_occupancy()
    print(x)