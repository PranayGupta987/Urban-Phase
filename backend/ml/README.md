# ML Dataset Preparation Pipeline

This directory contains the machine learning dataset preparation pipeline for UrbanPulse, designed to generate and process synthetic datasets for training congestion and pollution prediction models.

## 📁 Directory Structure

```
backend/ml/
├── dataset/
│   ├── traffic_data.csv      # Synthetic traffic data
│   ├── aqi_data.csv          # Synthetic AQI data
│   ├── weather_data.csv      # Synthetic weather data
│   └── merged_training_data.csv  # Merged training dataset
├── models/
│   ├── model.pkl            # Trained LightGBM model (generated)
│   ├── metrics.json         # Model evaluation metrics (generated)
│   └── sample_predictions.csv  # Sample predictions (generated)
├── prepare_dataset.py        # Dataset preparation pipeline
├── train_model.py           # Model training script
├── infer.py                 # Model inference script
├── features.py              # Feature engineering module
├── model_config.json        # ML model configuration
├── requirements-ml.txt      # ML-specific dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### 0. Install Dependencies

First, install required Python packages:

```bash
cd backend
pip install -r requirements.txt
```

Required packages: `pandas`, `numpy`, `scikit-learn`

### 1. Generate Datasets

Run the dataset preparation pipeline:

```bash
cd backend/ml
python prepare_dataset.py
```

This will:
- Generate synthetic traffic, AQI, and weather datasets (48 hours of data)
- Merge them into a unified training dataset
- Compute derived features
- Save all datasets as CSV files
- Print summary statistics

### 2. Dataset Schema

#### `traffic_data.csv`
- **timestamp**: DateTime (every 5 minutes)
- **segment_id**: Integer (1-200, representing road segments)
- **avg_speed**: Float (10-80 km/h)
- **congestion_level**: Float (0-1, normalized congestion)
- **vehicle_count**: Integer (50-300 vehicles)

#### `aqi_data.csv`
- **timestamp**: DateTime (every 5 minutes)
- **location_id**: Integer (1-50, representing monitoring stations)
- **pm25**: Float (10-200 µg/m³)
- **aqi**: Integer (50-200, Air Quality Index)

#### `weather_data.csv`
- **timestamp**: DateTime (every 5 minutes)
- **temperature**: Float (20-38°C)
- **humidity**: Float (40-95%)
- **wind_speed**: Float (0-40 km/h)
- **rainfall**: Float (0-20 mm)

#### `merged_training_data.csv`
Combines all three datasets with the following columns:
- **timestamp**: DateTime
- **segment_id**: Integer
- **avg_speed**: Float
- **congestion_level**: Float (target variable)
- **vehicle_count**: Integer
- **pm25**: Float
- **aqi**: Integer
- **temperature**: Float
- **humidity**: Float
- **wind_speed**: Float
- **rainfall**: Float
- **speed_drop**: Float (derived feature)
- **congestion_ratio**: Float (derived feature)
- **humidity_temp_interaction**: Float (derived feature)
- **traffic_density**: Float (derived feature)
- **pm25_dispersion**: Float (derived feature)
- **heat_index**: Float (derived feature)
- **weather_speed_impact**: Float (derived feature)

## 🔧 Feature Engineering

The `features.py` module provides:

### `compute_feature_matrix(df)`
Computes derived features from raw data:
- **speed_drop**: `max_speed_per_segment - current_speed`
- **congestion_ratio**: `vehicle_count / max(vehicle_count)`
- **humidity_temp_interaction**: `humidity * temperature`
- **traffic_density**: `vehicle_count / (avg_speed + 1)`
- **pm25_dispersion**: `pm25 / (wind_speed + 1)`
- **heat_index**: `temperature * (1 + humidity / 100)`
- **weather_speed_impact**: `avg_speed * (1 - rainfall / 10)`

### `scale_features(df, feature_columns, scaler_type)`
Scales features using StandardScaler or MinMaxScaler:
- **scaler_type**: `'standard'` or `'minmax'`
- Returns scaled DataFrame and scaler object

## 📊 Model Configuration

The `model_config.json` file specifies:
- **train_fraction**: 0.8 (80% for training, 20% for validation)
- **target_variable**: `"congestion_level"`
- **feature_columns**: List of features to use for training

## 🔄 Extending for Real Data

To use real data instead of synthetic data:

### Option 1: Replace CSV Generation
Modify `prepare_dataset.py` to load from your data sources:

```python
def generate_traffic_data(hours: int = 48) -> pd.DataFrame:
    # Replace with your API calls or database queries
    df = pd.read_sql("SELECT * FROM traffic_table", connection)
    return df
```

### Option 2: Direct CSV Replacement
Simply replace the generated CSV files with your real data files (matching the schema).

### Option 3: API Integration
Connect to the existing API clients in `backend/api_clients/`:

```python
from api_clients.traffic_api import fetch_live_traffic
from api_clients.aqi_api import fetch_live_aqi
from api_clients.weather_api import fetch_live_weather

# Fetch real data
traffic_geojson = fetch_live_traffic()
aqi_geojson = fetch_live_aqi()
weather_data = fetch_live_weather()
```

## 📈 Dataset Statistics

After running `prepare_dataset.py`, you'll see:
- Total number of records
- Time range covered
- Number of unique segments/locations
- Descriptive statistics for all features
- Missing value counts

## 🎯 Model Training

### 1. Set Up Environment

Create a virtual environment and install ML dependencies:

```bash
cd backend/ml
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate

# Install ML requirements
pip install -r requirements-ml.txt
```

### 2. Train the Model

Train a LightGBM regression model to predict congestion_level:

```bash
python train_model.py
```

This will:
- Load the merged training dataset
- Preprocess and engineer features
- Split into train/validation/test sets
- Train a LightGBM regressor with early stopping
- Evaluate on test set (RMSE and R²)
- Save model to `models/model.pkl`
- Save metrics to `models/metrics.json`

**Expected output:**
- Model trained and saved to `backend/ml/models/model.pkl`
- Training completes in under 5 minutes (uses up to 100k rows)

### 3. Run Inference

Test the trained model on sample data:

```bash
python infer.py
```

This will:
- Load the trained model
- Load 5 sample rows from the dataset
- Make predictions
- Print results with actual vs predicted values
- Save predictions to `models/sample_predictions.csv`

## 📊 Model Details

- **Algorithm**: LightGBM Gradient Boosting
- **Objective**: Regression (predict congestion_level)
- **Metric**: RMSE (Root Mean Squared Error)
- **Training**: 200 boosting rounds with early stopping (20 rounds)
- **Features**: Uses features from `model_config.json` plus engineered features

## 🔧 Next Steps

1. **Feature Selection**: Experiment with different feature combinations
2. **Hyperparameter Tuning**: Optimize model parameters
3. **Validation**: Evaluate on test set
4. **Deployment**: Integrate trained model into prediction API

## 📝 Notes

- Synthetic data includes realistic patterns (rush hours, day/night cycles)
- All datasets are aligned by timestamp (5-minute intervals)
- Missing values are forward-filled within a 2-interval window
- The pipeline is idempotent: re-running will use existing CSVs if available

## 🔗 Related Files

- `backend/api_clients/`: Real API connectors (can be integrated)
- `backend/models/schemas.py`: Data schemas
- `backend/services/`: Service layer for predictions
