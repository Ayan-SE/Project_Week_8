import pandas as pd
from flask import Flask, jsonify, request
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Load data (replace with your actual CSV file)
try:
    df = pd.read_csv('fraud_Data.csv')  # Make sure the path is correct
    # Ensure date column is datetime
    df['purchase_time'] = pd.to_datetime(df['purchase_time'])
    df['signup_time'] = pd.to_datetime(df['signup_time'])

    """
    if 'location' not in df.columns:
        df['location'] = 'Unknown'  # Replace with actual location data if available
    if 'device' not in df.columns:
        df['device'] = 'Unknown'
    if 'browser' not in df.columns:
        df['browser'] = 'Unknown'
    """
except FileNotFoundError:
    print("Error: fraud_data.csv not found. Please provide the correct path.")
    exit()  # Exit if the file isn't found


# Flask API endpoints
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

@app.route('/api/fraud_trends', methods=['GET'])
def fraud_trends():
    # Group by date and count fraud cases
    fraud_over_time = df[df['class'] == 1].groupby(df['purchase_time'].dt.date)['class'].count().reset_index()
    fraud_over_time.columns = ['date', 'fraud_count']  # Rename columns for clarity

    return jsonify(fraud_over_time.to_dict(orient='records')) # Return data as a list of dictionaries

@app.route('/api/fraud_by_location', methods=['GET'])
def fraud_by_location():
    fraud_by_location_data = df[df['class'] == 1].groupby('location')['class'].count().reset_index()
    fraud_by_location_data.columns = ['location', 'fraud_count']
    return jsonify(fraud_by_location_data.to_dict(orient='records'))

@app.route('/api/fraud_by_device_browser', methods=['GET'])
def fraud_by_device_browser():
    fraud_by_device = df[df['class'] == 1].groupby('device')['class'].count().reset_index()
    fraud_by_browser = df[df['class'] == 1].groupby('browser')['class'].count().reset_index()

    return jsonify({
        'device_data': fraud_by_device.to_dict(orient='records'),
        'browser_data': fraud_by_browser.to_dict(orient='records')
    })

# Dash layout
dash_app.layout = html.Div([
    html.H1("Fraud Detection Dashboard"),

    html.Div(id='summary-boxes', children=[
        # Summary boxes will be populated here
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),  # Arrange boxes horizontally

    dcc.Graph(id='fraud-over-time'),
    dcc.Graph(id='fraud-by-location'),
    dcc.Graph(id='fraud-by-device'),
    dcc.Graph(id='fraud-by-browser'),


    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )
])

# Dash callbacks
@dash_app.callback(
    Output('summary-boxes', 'children'),
    Input('interval-component', 'n_intervals')

)
def update_summary(n):

    summary_data = request.get('http://127.0.0.1:5000/api/summary').get_json()  # Get data from Flask API
    return [
        html.Div([html.H3("Total Transactions"), html.P(summary_data['total_transactions'])]),
        html.Div([html.H3("Fraud Cases"), html.P(summary_data['fraud_cases'])]),
        html.Div([html.H3("Fraud Percentage"), html.P(f"{summary_data['fraud_percentage']:.2f}%")])
    ]


@dash_app.callback(
    Output('fraud-over-time', 'figure'),
    Input('interval-component', 'n_intervals')

)
def update_fraud_over_time(n):
    trends_data = request.get('http://127.0.0.1:5000/api/fraud_trends').get_json()
    trends_df = pd.DataFrame(trends_data)
    fig = px.line(trends_df, x='date', y='fraud_count', title='Fraud Cases Over Time')
    return fig

@dash_app.callback(
    Output('fraud-by-location', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_fraud_by_location(n):
    location_data = request.get('http://127.0.0.1:5000/api/fraud_by_location').get_json()
    location_df = pd.DataFrame(location_data)
    fig = px.bar(location_df, x='location', y='fraud_count', title='Fraud Cases by Location')
    return fig

@dash_app.callback(
    Output('fraud-by-device', 'figure'),
    Output('fraud-by-browser', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_fraud_by_device_browser(n):
    device_browser_data = request.get('http://127.0.0.1:5000/api/fraud_by_device_browser').get_json()
    device_data = pd.DataFrame(device_browser_data['device_data'])
    browser_data = pd.DataFrame(device_browser_data['browser_data'])

    device_fig = px.bar(device_data, x='device', y='fraud_count', title='Fraud Cases by Device')
    browser_fig = px.bar(browser_data, x='browser', y='fraud_count', title='Fraud Cases by Browser')

    return device_fig, browser_fig

if __name__ == '__main__':
    # Run Flask app (API) in a separate thread
    import threading
    flask_thread = threading.Thread(target=app.run, kwargs={'debug': True, 'port': 5000, 'use_reloader': False}) #use_reloader=False for threading
    flask_thread.daemon = True #thread will close when main app closes
    flask_thread.start()

    # Run Dash app (Dashboard)
    dash_app.run_server(debug=True, port=8050)