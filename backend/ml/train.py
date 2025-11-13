import lightgbm as lgb
import pickle
from pathlib import Path
from ml.synthetic_data import generate_synthetic_data, split_data

def train_aqi_model():
    print("Generating synthetic training data...")
    df = generate_synthetic_data(n_samples=5000)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = split_data(df)

    print("Training LightGBM model...")
    model = lgb.LGBMRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        eval_metric='rmse'
    )

    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "aqi_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"Model saved to {model_path}")

    from sklearn.metrics import mean_squared_error, r2_score
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    print(f"Model Performance:")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  R²: {r2:.3f}")

    return model

if __name__ == "__main__":
    train_aqi_model()
