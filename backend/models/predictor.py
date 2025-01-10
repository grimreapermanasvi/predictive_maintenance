import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

class MaintenancePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.scaler = StandardScaler()
        self.is_trained = False

    def preprocess_data(self, data):
        features = np.array([[d['temperature'], d['vibration'], d['degradation']] for d in data])
        return self.scaler.transform(features) if self.is_trained else self.scaler.fit_transform(features)

    def train(self, historical_data):
        """Train the model with historical sensor data"""
        X = self.preprocess_data(historical_data)
        # Create labels based on the state
        y = np.array([1 if d['state'] in ['warning', 'critical'] else 0 for d in historical_data])
        
        self.model.fit(X, y)
        self.is_trained = True
        
    def predict(self, sensor_data):
        """Predict maintenance needs based on current sensor data"""
        if not self.is_trained:
            return {'status': 'error', 'message': 'Model not trained'}
            
        X = self.preprocess_data([sensor_data])
        prediction = self.model.predict(X)[0]
        proba = self.model.predict_proba(X)[0]
        
        return {
            'needs_maintenance': bool(prediction),
            'confidence': round(float(max(proba)), 3),
            'risk_level': 'high' if proba[1] > 0.7 else 'medium' if proba[1] > 0.4 else 'low'
        }

    def save_model(self, path='model.joblib'):
        """Save the trained model"""
        if self.is_trained:
            joblib.dump({'model': self.model, 'scaler': self.scaler}, path)

    def load_model(self, path='model.joblib'):
        """Load a trained model"""
        loaded = joblib.load(path)
        self.model = loaded['model']
        self.scaler = loaded['scaler']
        self.is_trained = True