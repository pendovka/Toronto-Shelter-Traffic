from merge_data import get_new_data
from sklearn.metrics import mean_absolute_error
from model import get_results

def mae(new_data, predictions_sarimax):

    return mean_absolute_error(new_data['unmatched_callers'][:len(predictions_sarimax)], predictions_sarimax)

def mae_repeated_last_observation_baseline(new_data):

    actual_values = new_data['unmatched_callers']
    baseline_predictions = actual_values.shift(1).ffill().tolist()  
    mae_baseline = mean_absolute_error(actual_values[1:], baseline_predictions[1:])
    
    return mae_baseline

def mae_comparison(new_data, predictions_sarimax):

    mae_last_observation = mae_repeated_last_observation_baseline(new_data).round(1)
    mae_sarimax = mae(new_data, predictions_sarimax).round(1)
    mae_comparison = (100 * (mae_last_observation - mae_sarimax) / mae_last_observation).round(1)

    mae_result = {'mae_last_observation': mae_last_observation,
                  'mae_sarimax': mae_sarimax,
                  'mae_comparison': mae_comparison}

    return {'mae_result': mae_result}

if __name__ == '__main__':
    x = mae_comparison(get_new_data(), get_results()['predictions'])
    print(x)
    

    