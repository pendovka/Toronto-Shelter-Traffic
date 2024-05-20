from model import get_results
from baseline_comparison import mae_comparison

def get_predictions():

    result = get_results()

    return {
        'predictions': result['predictions'],
        'actual_values': result['actual_values'],
        'dates': result['dates'],
        'comparison' : mae_comparison(result)['mae_result']
    }

if __name__ == '__main__':
    returned = get_predictions()
    print(returned)

    