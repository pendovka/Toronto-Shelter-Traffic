from extraction import fetch_data
import pandas as pd 

# REFRESHED DAILY

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

for variable in ['CAPACITY_ACTUAL_ROOM', 'CAPACITY_ACTUAL_BED', 'OCCUPANCY_RATE_BEDS', 'OCCUPANCY_RATE_ROOMS']:
    concatenated_occupancy[variable] = concatenated_occupancy[variable].fillna(0).astype(int)

concatenated_occupancy['occupancy_rate'] = concatenated_occupancy['OCCUPANCY_RATE_BEDS'] + concatenated_occupancy['OCCUPANCY_RATE_ROOMS']
concatenated_occupancy['capacity'] = concatenated_occupancy['CAPACITY_ACTUAL_ROOM'] + concatenated_occupancy['CAPACITY_ACTUAL_BED']

concatenated_occupancy = concatenated_occupancy.rename_axis('Date')

print(concatenated_occupancy)



