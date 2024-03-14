from extraction import fetch_data
import pandas as pd 

# REFRESHED MONTHLY. Data last refreshed: Feb 16, 2024. Latest Record: Jan 31st.

def get_calls():
    package_id_calls = "central-intake-calls"

    calls = fetch_data(package_id_calls, 6)

    calls['Date'] = pd.to_datetime(calls['Date'])

    calls.set_index('Date', inplace=True)  

    calls = calls.rename(columns={'Unmatched callers' : 'unmatched_callers'})
    calls = calls['unmatched_callers']
    calls = calls.to_frame(name='unmatched_callers')
    calls = calls[calls.index.year >= 2021] 
    return calls

x = get_calls()
print(x)