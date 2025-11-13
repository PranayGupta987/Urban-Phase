"""
Inference Script for UrbanPulse ML Model
Loads trained model and makes predictions on sample data
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# Import feature engineering functions
from features import compute_feature_matrix

# Paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "dataset"
MODELS_DIR = BASE_DIR / "models"
CONFIG_FILE = BASE_DIR / "model_config.json"

MODEL_FILE = MODELS_DIR / "model.pkl"
MERGED_CSV = DATASET_DIR / "merged_training_data.csv"
OUTPUT_CSV = MODELS_DIR / "sample_predictions.csv"


def load_model():
    """Load trained LightGBM model"""
    if not MODEL_FILE.exists():
        print(f"❌ ERROR: Model file not found: {MODEL_FILE}")
        print("\nPlease run 'python train_model.py' first to train the model.")
        exit(1)
    
    print(f"Loading model from {MODEL_FILE}...")
    model = joblib.load(MODEL_FILE)
    print("  ✓ Model loaded")
    return model


def load_sample_data(n_samples: int = 5):
    """Load sample rows from merged dataset"""
    if not MERGED_CSV.exists():
        print(f"❌ ERROR: Dataset file not found: {MERGED_CSV}")
        print("\nPlease run 'python prepare_dataset.py' first to generate the dataset.")
        exit(1)
    
    print(f"Loading sample data from {MERGED_CSV}...")
    df = pd.read_csv(MERGED_CSV, parse_dates=['timestamp'])
    
    # Take top N samples
    df_sample = df.head(n_samples).copy()
    print(f"  ✓ Loaded {len(df_sample)} sample rows")
    
    return df_sample


def preprocess_for_inference(df: pd.DataFrame, config: dict):
    """
    Preprocess data for inference (same as training pipeline)
    
    Args:
        df: DataFrame with sample data
        config: Model configuration
    
    Returns:
        Tuple of (preprocessed_df, feature_columns, target_values)
    """
    # Drop NaNs
    df = df.dropna()
    
    # Extract timestamp features
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['day_of_month'] = df['timestamp'].dt.day
    
    # Store target if available
    target = config.get('target_variable', 'congestion_level')
    target_values = None
    if target in df.columns:
        target_values = df[target].values
        # Don't drop target, we'll use it for comparison
    
    # Compute features
    df = compute_feature_matrix(df)
    
    # Get feature columns (same as training)
    base_features = config.get('feature_columns', [])
    timestamp_features = ['hour_of_day', 'day_of_week', 'day_of_month']
    
    all_features = []
    for feat in base_features + timestamp_features:
        if feat in df.columns:
            all_features.append(feat)
    
    # Add engineered features
    engineered_features = ['traffic_density', 'pm25_dispersion', 'heat_index', 'weather_speed_impact']
    for feat in engineered_features:
        if feat in df.columns and feat not in all_features:
            all_features.append(feat)
    
    return df, all_features, target_values


def main():
    """Main inference pipeline"""
    print("="*60)
    print("URBANPULSE MODEL INFERENCE")
    print("="*60)
    
    # Load config
    import json
    if not CONFIG_FILE.exists():
        print(f"❌ ERROR: Config file not found: {CONFIG_FILE}")
        exit(1)
    
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    # Load model
    model = load_model()
    
    # Load sample data
    df_sample = load_sample_data(n_samples=5)
    
    # Preprocess
    print("\nPreprocessing sample data...")
    df_processed, feature_columns, target_values = preprocess_for_inference(df_sample, config)
    
    # Extract features
    X_sample = df_processed[feature_columns]
    
    print(f"  ✓ Using {len(feature_columns)} features")
    
    # Make predictions
    print("\nMaking predictions...")
    predictions = model.predict(X_sample, num_iteration=model.best_iteration)
    
    # Create results DataFrame
    results = pd.DataFrame({
        'timestamp': df_sample['timestamp'].values[:len(predictions)],
        'segment_id': df_sample.get('segment_id', [None] * len(predictions)).values[:len(predictions)],
        'predicted_congestion_level': predictions
    })
    
    # Add actual values if available
    if target_values is not None and len(target_values) == len(predictions):
        results['actual_congestion_level'] = target_values[:len(predictions)]
        results['error'] = np.abs(results['predicted_congestion_level'] - results['actual_congestion_level'])
    
    # Print results
    print("\n" + "="*60)
    print("PREDICTION RESULTS")
    print("="*60)
    print("\n" + results.to_string(index=False))
    
    if 'actual_congestion_level' in results.columns:
        print(f"\nMean Absolute Error: {results['error'].mean():.4f}")
    
    # Save to CSV
    print(f"\nSaving predictions to {OUTPUT_CSV}...")
    results.to_csv(OUTPUT_CSV, index=False)
    print("  ✓ Predictions saved")
    
    print("\n" + "="*60)
    print("Inference complete!")
    print("="*60)


if __name__ == "__main__":
    main()

