import requests
from datetime import datetime
import json
import os

def save_to_json(file_path, new_data):
    # Load existing data or initialize an empty dictionary
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            existing_data_list = json.load(file)
        # Convert list of tuples to dictionary for easy update
        existing_data = {date: temp for date, temp in existing_data_list}
    else:
        existing_data = {}

    # Update existing_data with new_data
    for date, temp in new_data:
        existing_data[date] = temp

    # Convert the dictionary back to a list of tuples if necessary
    updated_data_list = [(date, temp) for date, temp in existing_data.items()]

    # Save updated data to JSON file
    with open(file_path, 'w') as file:
        json.dump(updated_data_list, file, indent=4)

def get_daily_min_temperatures_for_toronto_in_2023(api_key, lat=43.65107, lon=-79.347015):
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        daily_temperatures = []
        for daily_data in data['daily']:
            # Manually convert temperature from Kelvin to Celsius
            daily_temp = daily_data['temp']['min'] - 273.15
            # Format the date from the timestamp
            date = datetime.utcfromtimestamp(daily_data['dt']).strftime('%Y-%m-%d')
            daily_temperatures.append((date, daily_temp))
        return daily_temperatures
    else:
        print("Failed to retrieve data:", response.status_code)
        return None

api_key = '7d08c650b76cbb6f32017299ce1932e4'
file_path = 'toronto_daily_min_temperatures_2023.json'
toronto_daily_min_temperatures_2023 = get_daily_min_temperatures_for_toronto_in_2023(api_key)

if toronto_daily_min_temperatures_2023:
    save_to_json(file_path, toronto_daily_min_temperatures_2023)

    print("Updated data stored in JSON file.")
    with open(file_path, 'r') as file:
        stored_data = json.load(file)
    for date_temp in stored_data:
        print(f"{date_temp[0]} {date_temp[1]:.2f}")






2024-03-14 6.03
2024-03-15 5.47
2024-03-16 3.11
2024-03-17 2.94
2024-03-18 -0.77
2024-03-19 -2.20
2024-03-20 -0.05
2024-03-21 3.03




