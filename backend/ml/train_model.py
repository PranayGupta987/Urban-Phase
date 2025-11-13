"""
LightGBM Model Training Pipeline for UrbanPulse
Trains a regression model to predict congestion_level
"""
import os
import json
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import lightgbm as lgb

# Import feature engineering functions
from features import compute_feature_matrix, scale_features

# Paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "dataset"
MODELS_DIR = BASE_DIR / "models"
CONFIG_FILE = BASE_DIR / "model_config.json"

# Ensure models directory exists
MODELS_DIR.mkdir(exist_ok=True)

MERGED_CSV = DATASET_DIR / "merged_training_data.csv"
MODEL_FILE = MODELS_DIR / "model.pkl"
METRICS_FILE = MODELS_DIR / "metrics.json"


def load_and_preprocess_data(csv_path: Path, max_rows: int = 100000) -> pd.DataFrame:
    """
    Load and preprocess the merged training dataset
    
    Args:
        csv_path: Path to merged_training_data.csv
        max_rows: Maximum number of rows to use (for faster training)
    
    Returns:
        Preprocessed DataFrame
    """
    print(f"Loading dataset from {csv_path}...")
    
    if not csv_path.exists():
        print(f"\n❌ ERROR: Dataset file not found: {csv_path}")
        print("\nPlease run 'python prepare_dataset.py' first to generate the dataset.")
        exit(1)
    
    # Load dataset
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    print(f"  ✓ Loaded {len(df):,} rows")
    
    # Sample if dataset is too large
    if len(df) > max_rows:
        print(f"  ⚠ Dataset is large ({len(df):,} rows), sampling {max_rows:,} rows for faster training...")
        df = df.sample(n=max_rows, random_state=42).reset_index(drop=True)
        print(f"  ✓ Sampled to {len(df):,} rows")
    
    # Drop rows with NaNs
    initial_rows = len(df)
    df = df.dropna()
    dropped = initial_rows - len(df)
    if dropped > 0:
        print(f"  ✓ Dropped {dropped:,} rows with missing values")
    
    # Convert timestamp to features
    print("  ✓ Extracting timestamp features...")
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['day_of_month'] = df['timestamp'].dt.day
    
    # Drop timestamp column (we've extracted features)
    df = df.drop('timestamp', axis=1)
    
    print(f"  ✓ Preprocessed dataset: {len(df):,} rows, {len(df.columns)} columns")
    return df


def prepare_features(df: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, list]:
    """
    Prepare feature matrix using feature engineering
    
    Args:
        df: Preprocessed DataFrame
        config: Model configuration dictionary
    
    Returns:
        Tuple of (feature_df, feature_column_names)
    """
    print("\nComputing feature matrix...")
    
    # Compute derived features
    df = compute_feature_matrix(df)
    print("  ✓ Computed derived features")
    
    # Get base feature columns from config
    base_features = config.get('feature_columns', [])
    
    # Add timestamp features
    timestamp_features = ['hour_of_day', 'day_of_week', 'day_of_month']
    
    # Collect all available features
    all_features = []
    for feat in base_features + timestamp_features:
        if feat in df.columns:
            all_features.append(feat)
        else:
            print(f"  ⚠ Warning: Feature '{feat}' not found in dataset, skipping")
    
    # Also include any additional engineered features that might be useful
    engineered_features = ['traffic_density', 'pm25_dispersion', 'heat_index', 'weather_speed_impact']
    for feat in engineered_features:
        if feat in df.columns and feat not in all_features:
            all_features.append(feat)
    
    print(f"  ✓ Using {len(all_features)} features: {', '.join(all_features[:10])}{'...' if len(all_features) > 10 else ''}")
    
    return df, all_features


def train_lightgbm(X_train: pd.DataFrame, y_train: pd.Series,
                   X_val: pd.DataFrame, y_val: pd.Series) -> lgb.Booster:
    """
    Train LightGBM regression model
    
    Args:
        X_train: Training features
        y_train: Training target
        X_val: Validation features
        y_val: Validation target
    
    Returns:
        Trained LightGBM model
    """
    print("\nTraining LightGBM model...")
    
    # Convert to LightGBM Dataset format
    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
    
    # Hyperparameters
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': -1
    }
    
    print("  Hyperparameters:")
    print(f"    - objective: {params['objective']}")
    print(f"    - metric: {params['metric']}")
    print(f"    - num_leaves: {params['num_leaves']}")
    print(f"    - learning_rate: {params['learning_rate']}")
    
    # Train model
    model = lgb.train(
        params,
        train_data,
        num_boost_round=200,
        valid_sets=[train_data, val_data],
        valid_names=['train', 'eval'],
        callbacks=[lgb.early_stopping(stopping_rounds=20), lgb.log_evaluation(period=50)]
    )
    
    print("  ✓ Model training complete")
    return model


def evaluate_model(model: lgb.Booster, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """
    Evaluate model on test set
    
    Args:
        model: Trained LightGBM model
        X_test: Test features
        y_test: Test target
    
    Returns:
        Dictionary with metrics
    """
    print("\nEvaluating on test set...")
    
    # Make predictions
    y_pred = model.predict(X_test, num_iteration=model.best_iteration)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"  ✓ RMSE: {rmse:.4f}")
    print(f"  ✓ R² Score: {r2:.4f}")
    
    return {
        'rmse': float(rmse),
        'r2': float(r2),
        'best_iteration': int(model.best_iteration)
    }


def main():
    """Main training pipeline"""
    print("="*60)
    print("URBANPULSE LIGHTGBM MODEL TRAINING")
    print("="*60)
    
    # Load configuration
    if not CONFIG_FILE.exists():
        print(f"\n❌ ERROR: Config file not found: {CONFIG_FILE}")
        exit(1)
    
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    print(f"\n✓ Loaded config from {CONFIG_FILE}")
    print(f"  Target variable: {config['target_variable']}")
    print(f"  Train fraction: {config['train_fraction']}")
    
    # Load and preprocess data
    df = load_and_preprocess_data(MERGED_CSV, max_rows=100000)
    
    # Prepare features
    df, feature_columns = prepare_features(df, config)
    
    # Get target variable
    target = config['target_variable']
    if target not in df.columns:
        print(f"\n❌ ERROR: Target variable '{target}' not found in dataset")
        print(f"Available columns: {', '.join(df.columns.tolist())}")
        exit(1)
    
    # Extract features and target
    X = df[feature_columns]
    y = df[target]
    
    print(f"\nDataset shape: {X.shape}")
    print(f"Target variable: {target} (range: {y.min():.3f} to {y.max():.3f})")
    
    # Split into train/test
    train_fraction = config.get('train_fraction', 0.8)
    print(f"\nSplitting data (train: {train_fraction:.0%}, test: {1-train_fraction:.0%})...")
    
    # For time-series, we don't shuffle (use shuffle=False)
    # But for demo purposes, we'll use a simple split
    split_idx = int(len(X) * train_fraction)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    # Further split training data for validation
    val_fraction = 0.2
    val_split_idx = int(len(X_train) * (1 - val_fraction))
    X_train_split, X_val = X_train.iloc[:val_split_idx], X_train.iloc[val_split_idx:]
    y_train_split, y_val = y_train.iloc[:val_split_idx], y_train.iloc[val_split_idx:]
    
    print(f"  ✓ Train: {len(X_train_split):,} rows")
    print(f"  ✓ Validation: {len(X_val):,} rows")
    print(f"  ✓ Test: {len(X_test):,} rows")
    
    # Train model
    model = train_lightgbm(X_train_split, y_train_split, X_val, y_val)
    
    # Evaluate on test set
    metrics = evaluate_model(model, X_test, y_test)
    
    # Save model
    print(f"\nSaving model to {MODEL_FILE}...")
    joblib.dump(model, MODEL_FILE)
    print("  ✓ Model saved")
    
    # Save metrics
    print(f"Saving metrics to {METRICS_FILE}...")
    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f, indent=2)
    print("  ✓ Metrics saved")
    
    print("\n" + "="*60)
    print("Model trained and saved to backend/ml/models/model.pkl")
    print("="*60)
    print(f"\nFinal Metrics:")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  R²: {metrics['r2']:.4f}")
    print(f"  Best iteration: {metrics['best_iteration']}")


if __name__ == "__main__":
    main()

