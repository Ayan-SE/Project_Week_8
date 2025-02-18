from flask import Flask,render_template, request, jsonify
import pickle
import numpy as np
import logging 

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='fraud_detection.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

#@app.route('/')
#def home():
#   return render_template(index.html)

# Load the trained model
try:
    with open('linear_regression_model.pkl', 'rb') as f:
        model = pickle.load(f)
    logging.info("Model loaded successfully.")
except FileNotFoundError:
    logging.error("Model file not found!")
    exit(1)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        logging.info(f"Received request: {data}")  # Log the incoming request

        # Data validation (important!)
        if not all(key in data for key in ['feature1', 'feature2', 'feature3', '...']): # Replace with your actual feature names
            return jsonify({'error': 'Missing features in request'}), 400

        # Preprocessing (if needed)
        # Example: Convert data to numpy array and handle missing values
        input_data = np.array([data['feature1'], data['feature2'], data['feature3'], ...]).reshape(1, -1) # Adapt to your model's input

        # Prediction
        prediction = model.predict(input_data)[0]

        # Log the prediction
        logging.info(f"Prediction: {prediction}")

        # Response
        result = {'prediction': int(prediction)} # Convert to int for JSON serialization
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') # host='0.0.0.0' for Docker