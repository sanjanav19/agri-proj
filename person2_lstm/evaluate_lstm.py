import os
import pandas as pd
import numpy as np

from tensorflow.keras.models import load_model
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Paths
DATA_DIR = "processed"
MODEL_PATH = "models/lstm_model.keras"
RESULTS_DIR = "person2_lstm/results"

os.makedirs(RESULTS_DIR, exist_ok=True)

# Load test data
X_test = pd.read_csv(f"{DATA_DIR}/X_test.csv").values.astype("float32")
y_test = pd.read_csv(f"{DATA_DIR}/y_test.csv").values.astype("float32").ravel()

# Reshape for LSTM
X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])

print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)

# Load trained model
model = load_model(MODEL_PATH)

# Predict
y_pred = model.predict(X_test).ravel()

# Metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n===== TEST RESULTS =====")
print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")

# Save metrics
metrics = pd.DataFrame({
    "Metric": ["MAE", "MSE", "RMSE", "R2"],
    "Value": [mae, mse, rmse, r2]
})

metrics.to_csv(
    f"{RESULTS_DIR}/metrics.csv",
    index=False
)

# Save predictions
predictions = pd.DataFrame({
    "Actual": y_test,
    "Predicted": y_pred
})

predictions.to_csv(
    f"{RESULTS_DIR}/predictions.csv",
    index=False
)

print("\nMetrics saved to:", f"{RESULTS_DIR}/metrics.csv")
print("Predictions saved to:", f"{RESULTS_DIR}/predictions.csv")