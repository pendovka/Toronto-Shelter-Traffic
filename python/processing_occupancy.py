from extraction import fetch_data
import pandas as pd 
import numpy as np

# REFRESHED DAILY

def get_occupancy():

    package_id_occupancy = "daily-shelter-overnight-service-occupancy-capacity"

    occupancy2024 = fetch_data(package_id_occupancy, 0)
    occupancy2023 = fetch_data(package_id_occupancy, 1)
    occupancy2022 = fetch_data(package_id_occupancy, 2)
    occupancy2021 = fetch_data(package_id_occupancy, 3)

    occupancy2021['OCCUPANCY_DATE'] = pd.to_datetime(occupancy2021['OCCUPANCY_DATE'], format='%y-%m-%d').dt.strftime('%Y-%m-%d')
    occupancy2022['OCCUPANCY_DATE'] = pd.to_datetime(occupancy2022['OCCUPANCY_DATE'], format='%y-%m-%d').dt.strftime('%Y-%m-%d')
    occupancy2023['OCCUPANCY_DATE'] = pd.to_datetime(occupancy2023['OCCUPANCY_DATE'])
    occupancy2024['OCCUPANCY_DATE'] = pd.to_datetime(occupancy2024['OCCUPANCY_DATE'])

    concatenated_occupancy = pd.concat([occupancy2024, occupancy2023, occupancy2022, occupancy2021])
    concatenated_occupancy['OCCUPANCY_DATE'] = pd.to_datetime(concatenated_occupancy['OCCUPANCY_DATE'])

    concatenated_occupancy.sort_values(by='OCCUPANCY_DATE', inplace=True)
    concatenated_occupancy.set_index('OCCUPANCY_DATE', inplace=True)
    concatenated_occupancy = concatenated_occupancy.rename_axis('Date')

    concatenated_occupancy.fillna(0, inplace=True)

    concatenated_occupancy['occupancy_rate'] = concatenated_occupancy['OCCUPANCY_RATE_BEDS'] + concatenated_occupancy['OCCUPANCY_RATE_ROOMS']

    daily_mean_occupancy_rate = concatenated_occupancy['occupancy_rate'].resample('D').mean()
    concatenated_occupancy = daily_mean_occupancy_rate.to_frame(name='occupancy_rate')

    concatenated_occupancy['occupancy_rate_lag_day'] = concatenated_occupancy['occupancy_rate'].shift(1)
    concatenated_occupancy['occupancy_rate_lag_day'] = concatenated_occupancy['occupancy_rate_lag_day'].ffill()
    concatenated_occupancy['occupancy_rate_lag_day'] = concatenated_occupancy['occupancy_rate_lag_day'].bfill()
    concatenated_occupancy['occupancy_rate_lag_day'] = np.log(concatenated_occupancy['occupancy_rate_lag_day'])

    occupancy = concatenated_occupancy.drop(columns  = ['occupancy_rate'])
    
    return occupancy

