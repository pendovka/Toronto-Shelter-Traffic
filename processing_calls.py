from extraction import fetch_data
import pandas as pd 

# REFRESHED MONTHLY

def get_calls():
    
    package_id_calls = "central-intake-calls"

    calls = fetch_data(package_id_calls, 6)


    calls['Date'] = pd.to_datetime(calls['Date'])

    calls.set_index('Date', inplace=True)  
    calls = calls[calls.index.year >= 2024] 

    calls = calls.rename(columns={'Unmatched callers' : 'unmatched_callers'})
    calls = calls['unmatched_callers']
    calls = calls.to_frame(name='unmatched_callers')

    return calls

if __name__ == '__main__':
    x = get_calls()
    print(x)