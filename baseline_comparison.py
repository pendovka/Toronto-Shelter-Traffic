from merge_data import merge
from sklearn.metrics import mean_absolute_error
from model import get_predictions

def mae(new_data):

    predictions_sarimax = get_predictions()['predictions']

    return mean_absolute_error(new_data['unmatched_callers'][:len(predictions_sarimax)], predictions_sarimax)


def mae_repeated_last_observation_baseline(new_data):

    actual_values = new_data['unmatched_callers']
    baseline_predictions = actual_values.shift(1).bfill().tolist()
    mae_baseline = mean_absolute_error(actual_values[1:], baseline_predictions[1:])
    
    return mae_baseline

def comparison():

    new_data = merge()

    mae_last_observation = mae_repeated_last_observation_baseline(new_data)
    mae_sarimax = mae(new_data)

    print(f"MAE for baseline prediction using last observation: {mae_last_observation.round(2)}")
    print(f"MAE  for our model: {mae_sarimax.round(2)}")
    print(f"MAE improvement: {100 * (mae_last_observation - mae_sarimax) / mae_last_observation:.2f}%")


if __name__ == '__main__':
    comparison()
