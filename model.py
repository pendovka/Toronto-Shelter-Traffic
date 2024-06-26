from joblib import load
from merge_data import get_new_data
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

def get_results():

    new_data = get_new_data()

    current_features = ['min_temp_cels', 'occupancy_rate_lag_day']

    new_data_y = new_data.unmatched_callers
    new_data_exog = new_data[current_features]

    history_endog = new_data_y[:14].tolist()
    history_exog = new_data_exog[:14].values.tolist()

    predictions_sarimax = []
    actual_values = []

    for t in range(14, len(new_data)):

        model = SARIMAX(history_endog, exog=history_exog,
                        order=(1, 1, 1),  
                        seasonal_order=(1, 0, 1, 7))
        
        model_fit = model.fit(disp = 0)
        next_exog = new_data_exog.iloc[t:t+1].values  
        output = model_fit.forecast(exog=next_exog)
        yhat = round(float(output[0]))
        predictions_sarimax.append(yhat)
        obs = int(new_data_y.iloc[t])
        history_endog.append(obs)
        actual_values.append(obs)  
        history_exog.append(next_exog[0].tolist()) 

        print(f'*** CALCULATED {t+1}/{len(new_data)} ROWS ***') 
    
    date_strings = new_data.index[14:].strftime('%Y-%m-%d').tolist()
    
    return {
        'predictions': predictions_sarimax[:-1],
        'actual_values': actual_values[:-1],
        'dates': date_strings[:-1],
        'new_data': new_data[:-1]
    }


if __name__ == '__main__':
    x = get_results() 
    print(x)