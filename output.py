from model import get_results
from baseline_comparison import mae_comparison

def get_predictions():

    result = get_results()
    comparison = mae_comparison(result['new_data'],result['predictions'])['mae_result']

    return {
        'predictions': result['predictions'],
        'actual_values': result['actual_values'],
        'dates': result['dates'],
        'comparison' : comparison
    }

if __name__ == '__main__':
    returned = get_predictions()
    print(returned)

