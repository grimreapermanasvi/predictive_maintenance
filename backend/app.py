from flask import Flask, jsonify, request
from flask_cors import CORS
from simulator.sensor_simulator import SensorSimulator
from models.predictor import MaintenancePredictor
import threading
import time
import queue

app = Flask(__name__)
CORS(app)

# Global objects
simulator = SensorSimulator()
predictor = MaintenancePredictor()
data_queue = queue.Queue(maxsize=1000)
historical_data = []

def generate_data():
    """Background thread to generate sensor data"""
    while True:
        data = simulator.generate_sensor_data()
        if len(historical_data) >= 1000:
            historical_data.pop(0)
        historical_data.append(data)
        
        # Train model periodically
        if len(historical_data) % 100 == 0:
            predictor.train(historical_data)
            
        try:
            if data_queue.full():
                data_queue.get()  # Remove oldest data point
            data_queue.put(data)
        except queue.Full:
            pass
            
        time.sleep(1)  # Generate data every second

# Start data generation in background
threading.Thread(target=generate_data, daemon=True).start()

@app.route('/api/current-data')
def get_current_data():
    """Get the latest sensor readings and predictions"""
    try:
        sensor_data = data_queue.get_nowait()
        prediction = predictor.predict(sensor_data) if predictor.is_trained else {
            'needs_maintenance': False,
            'confidence': 0,
            'risk_level': 'unknown'
        }
        
        return jsonify({
            'sensor_data': sensor_data,
            'prediction': prediction
        })
    except queue.Empty:
        return jsonify({'error': 'No data available'}), 404

@app.route('/api/historical-data')
def get_historical_data():
    """Get historical sensor readings"""
    return jsonify(historical_data[-100:])  # Return last 100 readings

@app.route('/api/reset', methods=['POST'])
def reset_simulation():
    """Reset the simulator to healthy state"""
    simulator.reset()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)