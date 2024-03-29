from joblib import load
from merge_data import merge
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

def get_predictions():

    new_data = merge()
    current_features = ['min_temp_cels', 'occupancy_rate_lag_day']

    new_data_y = new_data.unmatched_callers
    new_data_exog = new_data[current_features]

    history_endog = load('old_unmatched.joblib')
    history_exog = load('old_exog.joblib')

    predictions_sarimax = []

    for t in range(len(new_data)):

        model = SARIMAX(history_endog, exog=history_exog,
                        order=(1, 1, 1),  
                        seasonal_order=(1, 0, 1, 7))
        
        model_fit = model.fit(disp = 0)
        next_exog = new_data_exog.iloc[t:t+1].values  
        output = model_fit.forecast(exog=next_exog)
        yhat = output[0]
        predictions_sarimax.append(yhat)
        obs = new_data_y.iloc[t]
        history_endog.append(obs)
        history_exog.append(next_exog[0].tolist())  

    return predictions_sarimax


def plot_predictions():

    new_data = merge()
    predictions_sarimax = get_predictions()

    plt.figure(figsize=(15, 7))
    plt.plot(new_data.index, new_data['unmatched_callers'], label='Actual Unmatched Callers', color='blue', marker='o')
    plt.plot(new_data.index[:len(predictions_sarimax)], predictions_sarimax, label='Predicted Unmatched Callers', color='red', linestyle='--', marker='x')

    plt.title('Actual vs Predicted Unmatched Callers')
    plt.xlabel('Date')
    plt.ylabel('Unmatched Callers')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    print(get_predictions())