from model import model
from baseline_comparison import mae_comparison

def get_predictions():

    predictions = model()['predictions']
    actual_values = model()['actual_values']
    dates = model()['dates']
    comparison = mae_comparison()['mae_result']


    return {
        'predictions': predictions,
        'actual_values': actual_values,
        'dates': dates,
        'comparison' : comparison
    }

if __name__ == '__main__':
    x = get_predictions()['comparison']
    print(x)