from flask import Flask, request, jsonify
from joblib import load

app = Flask(__name__)

# Load the model
model = load('model_filename.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Assuming 'data' is a dictionary with input features
    prediction = model.predict([data['features']])
    
    return jsonify(prediction=prediction.tolist())

if __name__ == '__main__':
    app.run(debug=True)
