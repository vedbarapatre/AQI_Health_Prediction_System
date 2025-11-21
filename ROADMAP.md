# 🚀 Full Functionality Implementation Roadmap
## AI-Based Air Quality & Health Prediction System (IHIP)

---

## Current Status ✅

**What's Working:**
- ✅ Complete UI/UX design (all 6 screens)
- ✅ Responsive layout (mobile + desktop)
- ✅ Dark mode toggle
- ✅ Sample data generation
- ✅ Interactive charts and maps
- ✅ Personal risk calculator
- ✅ Alert system UI
- ✅ Admin dashboard UI

**What's Next:**
Add real functionality, data integration, and AI models

---

## 🎯 Implementation Phases

### **Phase 1: Data Integration** (Priority: High)
Connect to real air quality data sources

### **Phase 2: AI Model Development** (Priority: High)
Build and train prediction models

### **Phase 3: Backend Services** (Priority: Medium)
Add database and API layer

### **Phase 4: Advanced Features** (Priority: Medium)
Enhance user experience

### **Phase 5: Deployment & Operations** (Priority: Low)
Production deployment and monitoring

---

## Phase 1: Data Integration 🔌

### 1.1 Real-Time Data Sources

#### Option A: CPCB API (Central Pollution Control Board)
**Implementation Steps:**

1. **Register for API Access**
   - Visit: https://app.cpcbccr.com/ccr_docs/
   - Register for API key
   - Documentation: https://api.data.gov.in/

2. **Create API Client Module**

```python
# Create: data_sources/cpcb_client.py

import requests
import pandas as pd
from datetime import datetime
import streamlit as st

class CPCBClient:
    """Client for CPCB air quality data"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.data.gov.in/resource/"
        
    def get_current_aqi(self, city):
        """Fetch current AQI for a city"""
        endpoint = f"{self.base_url}/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"
        
        params = {
            'api-key': self.api_key,
            'format': 'json',
            'filters[city]': city
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return self._parse_aqi_data(data)
        except Exception as e:
            st.error(f"Error fetching CPCB data: {str(e)}")
            return None
    
    def _parse_aqi_data(self, data):
        """Parse CPCB response"""
        if 'records' in data and len(data['records']) > 0:
            record = data['records'][0]
            return {
                'aqi': float(record.get('aqi', 0)),
                'pm25': float(record.get('pm2_5', 0)),
                'pm10': float(record.get('pm10', 0)),
                'timestamp': record.get('last_update', datetime.now())
            }
        return None

# Usage in app.py:
# @st.cache_data(ttl=300)  # Cache for 5 minutes
# def get_live_data(city):
#     client = CPCBClient(api_key=st.secrets["cpcb_api_key"])
#     return client.get_current_aqi(city)
```

#### Option B: OpenWeatherMap Air Pollution API
**Easier to start, free tier available**

```python
# Create: data_sources/openweather_client.py

import requests
import streamlit as st

class OpenWeatherClient:
    """Client for OpenWeather Air Pollution API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
    
    def get_current_aqi(self, lat, lon):
        """Fetch current AQI for coordinates"""
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'list' in data and len(data['list']) > 0:
                pollution = data['list'][0]
                components = pollution['components']
                
                return {
                    'aqi': pollution['main']['aqi'] * 50,  # Convert to 0-500 scale
                    'pm25': components.get('pm2_5', 0),
                    'pm10': components.get('pm10', 0),
                    'co': components.get('co', 0),
                    'no2': components.get('no2', 0),
                    'o3': components.get('o3', 0),
                    'timestamp': pollution['dt']
                }
        except Exception as e:
            st.error(f"Error fetching OpenWeather data: {str(e)}")
            return None
    
    def get_forecast(self, lat, lon):
        """Fetch 5-day air quality forecast"""
        url = f"{self.base_url}/forecast"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error fetching forecast: {str(e)}")
            return None

# Get free API key from: https://openweathermap.org/api
```

### 1.2 Historical Data Collection

```python
# Create: data_sources/data_collector.py

import pandas as pd
from datetime import datetime, timedelta
import schedule
import time

class DataCollector:
    """Collect and store historical data"""
    
    def __init__(self, db_path='data/aqi_history.db'):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Create SQLite database for historical data"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS aqi_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                aqi REAL,
                pm25 REAL,
                pm10 REAL,
                co REAL,
                no2 REAL,
                o3 REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_city_timestamp 
            ON aqi_readings(city, timestamp)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_reading(self, city, data):
        """Save a single reading to database"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO aqi_readings (city, aqi, pm25, pm10, co, no2, o3, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            city,
            data.get('aqi'),
            data.get('pm25'),
            data.get('pm10'),
            data.get('co', 0),
            data.get('no2', 0),
            data.get('o3', 0),
            data.get('source', 'api')
        ))
        
        conn.commit()
        conn.close()
    
    def get_historical_data(self, city, days=30):
        """Retrieve historical data for a city"""
        import sqlite3
        
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT timestamp, aqi, pm25, pm10
            FROM aqi_readings
            WHERE city = ? 
            AND timestamp >= datetime('now', '-' || ? || ' days')
            ORDER BY timestamp
        '''
        
        df = pd.read_sql_query(query, conn, params=(city, days))
        conn.close()
        
        return df
    
    def schedule_collection(self, cities, api_client):
        """Schedule automatic data collection"""
        def collect():
            for city in cities:
                data = api_client.get_current_aqi(city)
                if data:
                    self.save_reading(city, data)
        
        # Collect every hour
        schedule.every(1).hours.do(collect)
        
        while True:
            schedule.run_pending()
            time.sleep(60)
```

### 1.3 Configuration Management

```python
# Create: config.py

import os
from dataclasses import dataclass
from typing import List

@dataclass
class APIConfig:
    """API configuration"""
    openweather_api_key: str = ""
    cpcb_api_key: str = ""
    nasa_api_key: str = ""

@dataclass
class DatabaseConfig:
    """Database configuration"""
    sqlite_path: str = "data/aqi_history.db"
    backup_enabled: bool = True
    backup_interval_hours: int = 24

@dataclass
class AppConfig:
    """Application configuration"""
    cities: List[dict] = None
    default_city: str = "Delhi"
    data_refresh_interval: int = 300  # 5 minutes
    cache_ttl: int = 300
    
    def __post_init__(self):
        if self.cities is None:
            self.cities = [
                {'name': 'Delhi', 'lat': 28.6139, 'lon': 77.2090},
                {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777},
                {'name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946},
                {'name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639},
                {'name': 'Chennai', 'lat': 13.0827, 'lon': 80.2707},
                {'name': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867},
                {'name': 'Pune', 'lat': 18.5204, 'lon': 73.8567},
                {'name': 'Ahmedabad', 'lat': 23.0225, 'lon': 72.5714},
                {'name': 'Jaipur', 'lat': 26.9124, 'lon': 75.7873},
                {'name': 'Lucknow', 'lat': 26.8467, 'lon': 80.9462}
            ]

# Load from environment or secrets
def load_config():
    """Load configuration from environment/secrets"""
    import streamlit as st
    
    api_config = APIConfig(
        openweather_api_key=st.secrets.get("openweather_api_key", ""),
        cpcb_api_key=st.secrets.get("cpcb_api_key", ""),
        nasa_api_key=st.secrets.get("nasa_api_key", "")
    )
    
    return AppConfig(), api_config
```

---

## Phase 2: AI Model Development 🤖

### 2.1 Data Preparation

```python
# Create: ml_models/data_preparation.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class DataPreparation:
    """Prepare data for ML models"""
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def create_features(self, df):
        """Create time-based features"""
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Time features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.month
        df['day_of_year'] = df['timestamp'].dt.dayofyear
        
        # Lag features (previous values)
        for col in ['aqi', 'pm25', 'pm10']:
            df[f'{col}_lag_1h'] = df[col].shift(1)
            df[f'{col}_lag_24h'] = df[col].shift(24)
            df[f'{col}_lag_7d'] = df[col].shift(24*7)
        
        # Rolling statistics
        for col in ['aqi', 'pm25', 'pm10']:
            df[f'{col}_rolling_mean_24h'] = df[col].rolling(24).mean()
            df[f'{col}_rolling_std_24h'] = df[col].rolling(24).std()
        
        # Cyclical features
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        # Drop NaN values from lag features
        df = df.dropna()
        
        return df
    
    def prepare_sequences(self, data, sequence_length=24, forecast_horizon=24):
        """Prepare sequences for LSTM"""
        X, y = [], []
        
        for i in range(len(data) - sequence_length - forecast_horizon):
            X.append(data[i:i + sequence_length])
            y.append(data[i + sequence_length:i + sequence_length + forecast_horizon])
        
        return np.array(X), np.array(y)
    
    def split_data(self, X, y, test_size=0.2, val_size=0.1):
        """Split data into train, validation, and test sets"""
        # First split: train+val and test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, shuffle=False
        )
        
        # Second split: train and val
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size_adjusted, shuffle=False
        )
        
        return X_train, X_val, X_test, y_train, y_val, y_test
```

### 2.2 LSTM Model for Time-Series Prediction

```python
# Create: ml_models/lstm_model.py

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Optional: TensorFlow/Keras (install: pip install tensorflow)
"""
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

class LSTMPredictor:
    def __init__(self, sequence_length=24, forecast_horizon=24):
        self.sequence_length = sequence_length
        self.forecast_horizon = forecast_horizon
        self.model = None
    
    def build_model(self, input_shape):
        model = Sequential([
            LSTM(128, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(64, return_sequences=True),
            Dropout(0.2),
            LSTM(32),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dense(self.forecast_horizon)
        ])
        
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=32):
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        checkpoint = ModelCheckpoint(
            'models/lstm_best.h5',
            monitor='val_loss',
            save_best_only=True
        )
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, checkpoint],
            verbose=1
        )
        
        return history
    
    def predict(self, X):
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        
        metrics = {
            'rmse': np.sqrt(mean_squared_error(y_test.flatten(), y_pred.flatten())),
            'mae': mean_absolute_error(y_test.flatten(), y_pred.flatten()),
            'r2': r2_score(y_test.flatten(), y_pred.flatten())
        }
        
        return metrics
    
    def save(self, filepath='models/lstm_model.h5'):
        self.model.save(filepath)
    
    def load(self, filepath='models/lstm_model.h5'):
        self.model = keras.models.load_model(filepath)
"""
```

### 2.3 Random Forest Model (Alternative/Ensemble)

```python
# Create: ml_models/random_forest_model.py

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import joblib

class RandomForestPredictor:
    """Random Forest model for AQI prediction"""
    
    def __init__(self, n_estimators=100, max_depth=20):
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1
        )
    
    def train(self, X_train, y_train):
        """Train the model"""
        self.model.fit(X_train, y_train)
        return self
    
    def predict(self, X):
        """Make predictions"""
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        y_pred = self.predict(X_test)
        
        metrics = {
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'mae': mean_absolute_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred),
            'accuracy': self.calculate_accuracy(y_test, y_pred)
        }
        
        return metrics
    
    def calculate_accuracy(self, y_true, y_pred, tolerance=10):
        """Calculate prediction accuracy within tolerance"""
        within_tolerance = np.abs(y_true - y_pred) <= tolerance
        return np.mean(within_tolerance) * 100
    
    def get_feature_importance(self, feature_names):
        """Get feature importance"""
        importance = self.model.feature_importances_
        return pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
    
    def save(self, filepath='models/rf_model.pkl'):
        """Save model to disk"""
        joblib.dump(self.model, filepath)
    
    def load(self, filepath='models/rf_model.pkl'):
        """Load model from disk"""
        self.model = joblib.load(filepath)
        return self
```

### 2.4 Model Training Pipeline

```python
# Create: ml_models/train_pipeline.py

import pandas as pd
import numpy as np
from data_preparation import DataPreparation
from random_forest_model import RandomForestPredictor
import joblib

def train_aqi_model(data_path='data/aqi_history.db', city='Delhi'):
    """Complete training pipeline"""
    
    print(f"Training AQI prediction model for {city}...")
    
    # 1. Load data
    print("Loading data...")
    import sqlite3
    conn = sqlite3.connect(data_path)
    query = f"SELECT * FROM aqi_readings WHERE city = '{city}' ORDER BY timestamp"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # 2. Prepare features
    print("Creating features...")
    prep = DataPreparation()
    df_features = prep.create_features(df)
    
    # 3. Select features and target
    feature_cols = [col for col in df_features.columns 
                   if col not in ['timestamp', 'city', 'id', 'source', 'latitude', 'longitude']]
    target_col = 'aqi'
    
    X = df_features[feature_cols]
    y = df_features[target_col]
    
    # 4. Split data
    print("Splitting data...")
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # 5. Train model
    print("Training Random Forest model...")
    model = RandomForestPredictor(n_estimators=200, max_depth=30)
    model.train(X_train, y_train)
    
    # 6. Evaluate
    print("Evaluating model...")
    metrics = model.evaluate(X_test, y_test)
    
    print("\n=== Model Performance ===")
    print(f"RMSE: {metrics['rmse']:.2f}")
    print(f"MAE: {metrics['mae']:.2f}")
    print(f"R² Score: {metrics['r2']:.4f}")
    print(f"Accuracy (±10 AQI): {metrics['accuracy']:.2f}%")
    
    # 7. Save model
    print("\nSaving model...")
    model.save(f'models/{city.lower()}_rf_model.pkl')
    joblib.dump(feature_cols, f'models/{city.lower()}_features.pkl')
    
    # 8. Feature importance
    importance = model.get_feature_importance(feature_cols)
    print("\n=== Top 10 Important Features ===")
    print(importance.head(10))
    
    return model, metrics, importance

if __name__ == "__main__":
    # Train for all cities
    cities = ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Chennai']
    
    for city in cities:
        try:
            model, metrics, importance = train_aqi_model(city=city)
        except Exception as e:
            print(f"Error training model for {city}: {e}")
```

---

## Phase 3: Backend Services 💾

### 3.1 Database Schema

```python
# Create: database/schema.py

import sqlite3
from datetime import datetime

def create_database(db_path='data/aqi_system.db'):
    """Create complete database schema"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # AQI readings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aqi_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            aqi REAL,
            pm25 REAL,
            pm10 REAL,
            co REAL,
            no2 REAL,
            o3 REAL,
            so2 REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source TEXT,
            UNIQUE(city, timestamp)
        )
    ''')
    
    # User subscriptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            cities TEXT,  -- JSON array of cities
            alert_threshold INTEGER DEFAULT 100,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Alerts history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT,
            aqi_value REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Model performance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            city TEXT,
            rmse REAL,
            mae REAL,
            r2_score REAL,
            accuracy REAL,
            trained_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            forecast_date DATE NOT NULL,
            predicted_aqi REAL,
            confidence_interval_lower REAL,
            confidence_interval_upper REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(city, forecast_date)
        )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_city_timestamp ON aqi_readings(city, timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_alert_city ON alerts_history(city, created_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictions ON predictions(city, forecast_date)')
    
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at {db_path}")

if __name__ == "__main__":
    create_database()
```

### 3.2 Alert System

```python
# Create: services/alert_system.py

import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertSystem:
    """Manage and send alerts"""
    
    def __init__(self, db_path='data/aqi_system.db'):
        self.db_path = db_path
    
    def check_and_create_alerts(self, city, aqi_data):
        """Check if alerts should be created"""
        aqi = aqi_data['aqi']
        
        # Determine alert level
        if aqi > 200:
            severity = "Very High"
            alert_type = "Air Quality Alert"
            message = f"Hazardous air quality detected in {city}. AQI: {int(aqi)}. Avoid all outdoor activities."
        elif aqi > 150:
            severity = "High"
            alert_type = "Air Quality Alert"
            message = f"Unhealthy air quality in {city}. AQI: {int(aqi)}. Limit outdoor activities."
        elif aqi > 100:
            severity = "Medium"
            alert_type = "Health Risk Alert"
            message = f"Moderate air quality in {city}. AQI: {int(aqi)}. Sensitive groups should be cautious."
        else:
            return None  # No alert needed
        
        # Save alert to database
        self.save_alert(city, alert_type, severity, message, aqi)
        
        # Send notifications to subscribers
        self.notify_subscribers(city, alert_type, severity, message)
        
        return {
            'type': alert_type,
            'severity': severity,
            'message': message,
            'aqi': aqi
        }
    
    def save_alert(self, city, alert_type, severity, message, aqi_value):
        """Save alert to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts_history (city, alert_type, severity, message, aqi_value)
            VALUES (?, ?, ?, ?, ?)
        ''', (city, alert_type, severity, message, aqi_value))
        
        conn.commit()
        conn.close()
    
    def notify_subscribers(self, city, alert_type, severity, message):
        """Send notifications to subscribers"""
        subscribers = self.get_subscribers(city)
        
        for subscriber in subscribers:
            if subscriber['email']:
                self.send_email_alert(
                    subscriber['email'],
                    alert_type,
                    severity,
                    message
                )
            
            if subscriber['phone']:
                self.send_sms_alert(
                    subscriber['phone'],
                    message
                )
    
    def send_email_alert(self, to_email, alert_type, severity, message):
        """Send email alert (requires SMTP configuration)"""
        try:
            # Configure SMTP settings
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "ihip.alerts@example.com"
            sender_password = "your_app_password"
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = f"IHIP Alert: {alert_type} - {severity}"
            
            body = f"""
            <html>
            <body>
                <h2>{alert_type}</h2>
                <p><strong>Severity:</strong> {severity}</p>
                <p>{message}</p>
                <hr>
                <p><small>This is an automated alert from IHIP - Air Quality & Health Prediction System</small></p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            print(f"Email alert sent to {to_email}")
            
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def send_sms_alert(self, phone, message):
        """Send SMS alert (requires SMS gateway like Twilio)"""
        # Implement SMS sending using Twilio, AWS SNS, or other service
        pass
    
    def get_subscribers(self, city):
        """Get all active subscribers for a city"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT email, phone, cities, alert_threshold
            FROM user_subscriptions
            WHERE is_active = 1
        ''')
        
        subscribers = []
        for row in cursor.fetchall():
            import json
            cities = json.loads(row[2])
            if city in cities:
                subscribers.append({
                    'email': row[0],
                    'phone': row[1],
                    'threshold': row[3]
                })
        
        conn.close()
        return subscribers
    
    def subscribe_user(self, email, cities, phone=None, threshold=100):
        """Subscribe user to alerts"""
        import json
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO user_subscriptions (email, phone, cities, alert_threshold)
                VALUES (?, ?, ?, ?)
            ''', (email, phone, json.dumps(cities), threshold))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # User already subscribed, update instead
            cursor.execute('''
                UPDATE user_subscriptions
                SET cities = ?, alert_threshold = ?, is_active = 1
                WHERE email = ?
            ''', (json.dumps(cities), threshold, email))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error subscribing user: {e}")
            return False
        finally:
            conn.close()
```

---

## Phase 4: Advanced Features 🌟

### 4.1 Export Functionality

```python
# Create: utils/export.py

import pandas as pd
from datetime import datetime
import io

def export_to_csv(data, filename=None):
    """Export data to CSV"""
    if filename is None:
        filename = f"aqi_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False), filename

def export_to_excel(data, filename=None):
    """Export data to Excel"""
    if filename is None:
        filename = f"aqi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    df = pd.DataFrame(data)
    
    # Create Excel writer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='AQI Data', index=False)
        
        # Get workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['AQI Data']
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#667eea',
            'font_color': 'white',
            'border': 1
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)
    
    return output.getvalue(), filename

def generate_pdf_report(city, data, metrics):
    """Generate PDF report (requires reportlab)"""
    # Install: pip install reportlab
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>Air Quality Report - {city}</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Summary
    summary = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal'])
    elements.append(summary)
    elements.append(Spacer(1, 12))
    
    # Metrics table
    metrics_data = [
        ['Metric', 'Value'],
        ['Current AQI', f"{data['aqi']:.1f}"],
        ['PM2.5', f"{data['pm25']:.1f} μg/m³"],
        ['PM10', f"{data['pm10']:.1f} μg/m³"],
        ['Risk Level', data['risk_level']]
    ]
    
    table = Table(metrics_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    doc.build(elements)
    return output.getvalue()
```

### 4.2 Multi-language Support

```python
# Create: utils/translations.py

translations = {
    'en': {
        'app_title': 'AI-Based Air Quality & Health Prediction System',
        'home': 'Home',
        'map': 'Map',
        'trends': 'Trends',
        'calculator': 'Health Risk Calculator',
        'alerts': 'Alerts',
        'admin': 'Admin',
        'aqi': 'Air Quality Index',
        'current_aqi': 'Current AQI',
        'risk_level': 'Risk Level',
        'good': 'Good',
        'moderate': 'Moderate',
        'unhealthy': 'Unhealthy',
        'very_unhealthy': 'Very Unhealthy',
        'hazardous': 'Hazardous'
    },
    'hi': {
        'app_title': 'एआई-आधारित वायु गुणवत्ता और स्वास्थ्य पूर्वानुमान प्रणाली',
        'home': 'होम',
        'map': 'मानचित्र',
        'trends': 'रुझान',
        'calculator': 'स्वास्थ्य जोखिम कैलकुलेटर',
        'alerts': 'अलर्ट',
        'admin': 'व्यवस्थापक',
        'aqi': 'वायु गुणवत्ता सूचकांक',
        'current_aqi': 'वर्तमान एक्यूआई',
        'risk_level': 'जोखिम स्तर',
        'good': 'अच्छा',
        'moderate': 'मध्यम',
        'unhealthy': 'अस्वास्थ्यकर',
        'very_unhealthy': 'बहुत अस्वास्थ्यकर',
        'hazardous': 'खतरनाक'
    }
}

def get_text(key, language='en'):
    """Get translated text"""
    return translations.get(language, translations['en']).get(key, key)
```

---

## Phase 5: Deployment & Operations 🚀

### 5.1 Streamlit Cloud Deployment

```bash
# Create: .streamlit/config.toml

[theme]
primaryColor = "#667eea"
backgroundColor = "#F7FAFC"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#2C3E50"
font = "sans serif"

[server]
headless = true
enableCORS = false
port = 8501

[browser]
gatherUsageStats = false
```

```toml
# Create: .streamlit/secrets.toml (DO NOT COMMIT TO GIT)

openweather_api_key = "your_api_key_here"
cpcb_api_key = "your_api_key_here"
nasa_api_key = "your_api_key_here"

[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "alerts@example.com"
sender_password = "your_app_password"
```

### 5.2 Docker Deployment

```dockerfile
# Create: Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```yaml
# Create: docker-compose.yml

version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}
      - CPCB_API_KEY=${CPCB_API_KEY}
    restart: unless-stopped
  
  data-collector:
    build: .
    command: python data_sources/data_collector.py
    volumes:
      - ./data:/app/data
    environment:
      - OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}
    restart: unless-stopped
```

### 5.3 GitHub Actions CI/CD

```yaml
# Create: .github/workflows/deploy.yml

name: Deploy to Production

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Streamlit Cloud
        run: |
          # Add deployment script here
          echo "Deploying to Streamlit Cloud..."
```

---

## 📋 Quick Implementation Checklist

### Week 1: Data Integration
- [ ] Get OpenWeatherMap API key
- [ ] Create `data_sources/` folder structure
- [ ] Implement OpenWeather client
- [ ] Set up database schema
- [ ] Start collecting historical data
- [ ] Update app.py to use real data

### Week 2: ML Models
- [ ] Prepare training data
- [ ] Train Random Forest model
- [ ] Evaluate model performance
- [ ] Save trained models
- [ ] Integrate predictions into app

### Week 3: Backend Services
- [ ] Implement alert system
- [ ] Add email notifications
- [ ] Create subscription management
- [ ] Add export functionality

### Week 4: Deployment
- [ ] Set up Streamlit Cloud account
- [ ] Configure secrets
- [ ] Deploy application
- [ ] Test in production
- [ ] Monitor performance

---

## 🎯 Priority Actions (Start Today!)

1. **Get API Key** (5 minutes)
   - Register at: https://openweathermap.org/api
   - Free tier: 1,000 calls/day

2. **Create Directory Structure** (2 minutes)
   ```bash
   mkdir data_sources ml_models services utils database models data tests
   ```

3. **Install Additional Dependencies** (3 minutes)
   ```bash
   pip install requests schedule scikit-learn joblib
   ```

4. **Start Data Collection** (10 minutes)
   - Copy OpenWeather client code
   - Add API key to secrets
   - Test data fetching

5. **Update app.py** (15 minutes)
   - Replace sample data with real API calls
   - Add caching

---

## 📚 Additional Resources

- **OpenWeatherMap API Docs:** https://openweathermap.org/api/air-pollution
- **CPCB Data Portal:** https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing
- **Scikit-learn Docs:** https://scikit-learn.org/stable/
- **Streamlit Deployment:** https://docs.streamlit.io/streamlit-community-cloud/get-started
- **Docker Tutorial:** https://docs.docker.com/get-started/

---

## 💬 Need Help?

Create detailed implementation guides for any phase:
1. Data integration
2. ML model training
3. Alert system setup
4. Deployment process

Just ask: "Show me detailed code for [Phase X]"

---

<div align="center">

**Ready to build a production-ready AQI system!** 🚀

Start with Phase 1: Get your API key and begin data collection today!

</div>
