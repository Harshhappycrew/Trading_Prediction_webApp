"""
LSTM Price Prediction Model
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import MinMaxScaler
import joblib
from loguru import logger
from pathlib import Path

class LSTMPredictor:
    """LSTM model for stock price prediction"""
    
    def __init__(self, sequence_length: int = 15, features: int = 10):
        self.sequence_length = sequence_length
        self.features = features
        self.model = None
        self.scaler = MinMaxScaler()
        self.model_path = Path("data/models/lstm_predictor.h5")
        self.scaler_path = Path("data/models/lstm_scaler.pkl")
    
    def build_model(self):
        """Build LSTM model architecture"""
        model = keras.Sequential([
            layers.LSTM(50, return_sequences=True, input_shape=(self.sequence_length, self.features)),
            layers.Dropout(0.2),
            layers.LSTM(50, return_sequences=False),
            layers.Dropout(0.2),
            layers.Dense(25, activation='relu'),
            layers.Dense(1)
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        logger.info("LSTM model built successfully")
        return model
    
    def prepare_sequences(self, data: np.ndarray):
        """Prepare sequences for LSTM training"""
        X, y = [], []
        
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i + self.sequence_length])
            y.append(data[i + self.sequence_length, 0])  # Predict close price
        
        return np.array(X), np.array(y)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, epochs: int = 50, batch_size: int = 32):
        """Train the LSTM model"""
        if self.model is None:
            self.build_model()
        
        # Scale data
        X_train_scaled = self.scaler.fit_transform(X_train.reshape(-1, self.features)).reshape(X_train.shape)
        
        history = self.model.fit(
            X_train_scaled,
            y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=1
        )
        
        logger.info("LSTM training completed")
        return history
    
    def predict(self, X: np.ndarray):
        """Make predictions"""
        if self.model is None:
            self.load_model()
        
        X_scaled = self.scaler.transform(X.reshape(-1, self.features)).reshape(X.shape)
        predictions = self.model.predict(X_scaled, verbose=0)
        
        return predictions
    
    def save_model(self):
        """Save model and scaler"""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        self.model.save(self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load model and scaler"""
        if self.model_path.exists():
            self.model = keras.models.load_model(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            logger.info("Model loaded successfully")
        else:
            logger.warning("No saved model found, building new model")
            self.build_model()
