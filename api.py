from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load your data (replace with your actual data loading)
try:
    df = pd.read_csv("fraud_data.csv")  # Replace with your CSV path
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['date'] = df['transaction_date'].dt.date
except FileNotFoundError:
    print("Error: fraud_data.csv not found. Please provide the correct path.")
    exit()

# 1. Summary Statistics
@app.route('/api/summary', methods=['GET'])
def summary():
    total_transactions = len(df)
    fraud_cases = df['class'].sum()  # Assuming 'is_fraud' is a boolean or 1/0 column
    fraud_percentage = (fraud_cases / total_transactions) * 100 if total_transactions else 0
    return jsonify({
        'total_transactions': total_transactions,
        'fraud_cases': fraud_cases,
        'fraud_percentage': fraud_percentage
    })

# 2. Fraud Trends Over Time
@app.route('/api/fraud_trends', methods=['GET'])
def fraud_trends():
    fraud_over_time = df[df['class'] == 1].groupby('date')['class'].count().reset_index()
    fraud_over_time.columns = ['date', 'fraud_count']
    return jsonify(fraud_over_time.to_dict(orient='records'))  # Important: Return as a list of dictionaries

# 3. Fraud by Location (Example)
@app.route('/api/fraud_by_location', methods=['GET'])
def fraud_by_location():
    fraud_by_location = df[df['class'] == 1].groupby('location')['class'].count().reset_index()
    fraud_by_location.columns = ['location', 'fraud_count']
    return jsonify(fraud_by_location.to_dict(orient='records'))

# 4. Fraud by Device/Browser (Example)
@app.route('/api/fraud_by_device_browser', methods=['GET'])
def fraud_by_device_browser():
    fraud_by_device = df[df['class'] == 1].groupby('device')['class'].count().reset_index()
    fraud_by_browser = df[df['class'] == 1].groupby('browser')['class'].count().reset_index()
    return jsonify({
        'device_data': fraud_by_device.to_dict(orient='records'),
        'browser_data': fraud_by_browser.to_dict(orient='records')
    })

# 5.  (Optional) Fraud Details (For a table or more detailed view)
@app.route('/api/fraud_details', methods=['GET'])
def fraud_details():
    # You might want to add filtering or pagination here if you have a lot of data
    fraud_details = df[df['class'] == 1].to_dict(orient='records')  # All fraud cases
    return jsonify(fraud_details)


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Run Flask app
