from extraction import fetch_data
import pandas as pd 

# REFRESHED MONTHLY

package_id_calls = "central-intake-calls"

calls = fetch_data(package_id_calls, 6)

calls['Date'] = pd.to_datetime(calls['Date'])
calls.set_index('Date', inplace=True)  

calls = calls.rename(columns={'Unmatched callers' : 'unmatched_callers'})
