from merge_data import merge
from sklearn.metrics import mean_absolute_error
from model import get_predictions

def mae(new_data):

    predictions_sarimax = get_predictions()

    return mean_absolute_error(new_data['unmatched_callers'][:len(predictions_sarimax)], predictions_sarimax)


def mae_mean_baseline(new_data):

    mean_value = new_data['unmatched_callers'].mean()
    baseline_predictions = [mean_value] * len(new_data)
    mae_baseline = mean_absolute_error(new_data['unmatched_callers'], baseline_predictions)
    
    return mae_baseline
    

def mae_last_value_baseline(new_data_y, predictions_length):

    last_value = new_data_y.iloc[-1]
    baseline_predictions = [last_value] * predictions_length

    return mean_absolute_error(new_data_y[:predictions_length], baseline_predictions)


def mae_repeated_last_observation_baseline(new_data):

    actual_values = new_data['unmatched_callers']
    baseline_predictions = actual_values.shift(1).fillna(method='bfill').tolist()
    mae_baseline = mean_absolute_error(actual_values[1:], baseline_predictions[1:])
    
    return mae_baseline

def comparison():

    new_data = merge()

    mae_last_observation = mae_repeated_last_observation_baseline(new_data)
    mae_baseline = mae_mean_baseline(new_data)
    mae_sarimax = mae(new_data)

    print(f"MAE for baseline prediction using mean: {mae_baseline}")
    print(f"MAE for baseline prediction using last observation: {mae_last_observation}")
    print(f"MAE for our model: {mae_sarimax}")

comparison()