from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Load the model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../model/battery_model.pkl')

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"Failed to load model: {e}")
        model = None
else:
    print(f"Error: Model not found at {MODEL_PATH}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.get_json()
        
        # Expected features: voltage, current, temperature, cycle
        features = [
            data.get('voltage'),
            data.get('current'),
            data.get('temperature'),
            data.get('cycle')
        ]
        
        if None in features:
            return jsonify({'error': 'Missing input values'}), 400

        # Create DataFrame for prediction
        input_df = pd.DataFrame([features], columns=['voltage', 'current', 'temperature', 'cycle'])
        
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            'soh': float(prediction),
            'message': 'Prediction successful'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Real-time Simulation Storage ---
latest_sensor_data = {
    'voltage': 0,
    'current': 0,
    'temperature': 0,
    'cycle': 0,
    'soh': 0,
    'timestamp': None
}

@app.route('/update_sensor', methods=['POST'])
def update_sensor():
    """Receives data from the hardware simulator."""
    global latest_sensor_data
    try:
        data = request.get_json()
        
        # Predict SoH for this new data point
        features = pd.DataFrame([[
            data.get('voltage'),
            data.get('current'),
            data.get('temperature'),
            data.get('cycle')
        ]], columns=['voltage', 'current', 'temperature', 'cycle'])
        
        if model:
            pred_soh = model.predict(features)[0]
        else:
            pred_soh = 0

        latest_sensor_data = {
            'voltage': data.get('voltage'),
            'current': data.get('current'),
            'temperature': data.get('temperature'),
            'cycle': data.get('cycle'),
            'soh': float(pred_soh),
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        return jsonify({'message': 'Data received', 'soh': latest_sensor_data['soh']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Returns the latest sensor data and prediction."""
    return jsonify(latest_sensor_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
