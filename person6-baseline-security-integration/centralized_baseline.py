import os
import sys
import pandas as pd
import numpy as np

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(PROJECT_ROOT, "processed")
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")
RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "results"
)

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


# --------------------------------------------------
# 2. Import Person 2's LSTM model
# --------------------------------------------------

PERSON2_DIR = os.path.join(
    PROJECT_ROOT,
    "person2_lstm"
)

sys.path.append(PERSON2_DIR)

from lstm_model import create_lstm_model


# --------------------------------------------------
# 3. Configuration
# --------------------------------------------------

BATCH_SIZE = 32
EPOCHS = 100
SEED = 42

np.random.seed(SEED)


# --------------------------------------------------
# 4. Load processed data
# --------------------------------------------------

X_train = pd.read_csv(
    os.path.join(DATA_DIR, "X_train.csv")
).values.astype("float32")

X_val = pd.read_csv(
    os.path.join(DATA_DIR, "X_val.csv")
).values.astype("float32")

X_test = pd.read_csv(
    os.path.join(DATA_DIR, "X_test.csv")
).values.astype("float32")

y_train = pd.read_csv(
    os.path.join(DATA_DIR, "y_train.csv")
).values.astype("float32").ravel()

y_val = pd.read_csv(
    os.path.join(DATA_DIR, "y_val.csv")
).values.astype("float32").ravel()

y_test = pd.read_csv(
    os.path.join(DATA_DIR, "y_test.csv")
).values.astype("float32").ravel()


# --------------------------------------------------
# 5. Reshape data for LSTM
# --------------------------------------------------

X_train = X_train.reshape(
    X_train.shape[0],
    1,
    X_train.shape[1]
)

X_val = X_val.reshape(
    X_val.shape[0],
    1,
    X_val.shape[1]
)

X_test = X_test.reshape(
    X_test.shape[0],
    1,
    X_test.shape[1]
)

print("\nDataset shapes:")
print("X_train:", X_train.shape)
print("X_val  :", X_val.shape)
print("X_test :", X_test.shape)


# --------------------------------------------------
# 6. Create centralized LSTM model
# --------------------------------------------------

model = create_lstm_model(
    input_shape=(1, X_train.shape[2])
)

print("\nModel:")
model.summary()


# --------------------------------------------------
# 7. Callbacks
# --------------------------------------------------

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    os.path.join(
        MODEL_DIR,
        "centralized_lstm_model.keras"
    ),
    monitor="val_loss",
    save_best_only=True
)


# --------------------------------------------------
# 8. Train centralized model
# --------------------------------------------------

print("\nStarting centralized LSTM training...")

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=[
        early_stopping,
        checkpoint
    ],
    verbose=1
)

print("\nTraining completed.")


# --------------------------------------------------
# 9. Evaluate on test set
# --------------------------------------------------

print("\nEvaluating centralized model...")

y_pred = model.predict(
    X_test,
    verbose=0
).ravel()

mae = mean_absolute_error(
    y_test,
    y_pred
)

mse = mean_squared_error(
    y_test,
    y_pred
)

rmse = np.sqrt(mse)

r2 = r2_score(
    y_test,
    y_pred
)


# --------------------------------------------------
# 10. Display results
# --------------------------------------------------

print("\n========================================")
print("CENTRALIZED LSTM RESULTS")
print("========================================")
print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")
print("========================================")


# --------------------------------------------------
# 11. Save metrics
# --------------------------------------------------

metrics = pd.DataFrame([
    {
        "model": "Centralized LSTM",
        "mae": mae,
        "mse": mse,
        "rmse": rmse,
        "r2": r2
    }
])

metrics.to_csv(
    os.path.join(
        RESULTS_DIR,
        "centralized_metrics.csv"
    ),
    index=False
)


# --------------------------------------------------
# 12. Save predictions
# --------------------------------------------------

predictions = pd.DataFrame({
    "actual": y_test,
    "predicted": y_pred
})

predictions.to_csv(
    os.path.join(
        RESULTS_DIR,
        "centralized_predictions.csv"
    ),
    index=False
)


# --------------------------------------------------
# 13. Save training history
# --------------------------------------------------

history_df = pd.DataFrame(history.history)

history_df.to_csv(
    os.path.join(
        RESULTS_DIR,
        "centralized_training_history.csv"
    ),
    index=False
)


print("\nResults saved:")
print("- centralized_metrics.csv")
print("- centralized_predictions.csv")
print("- centralized_training_history.csv")
print("- centralized_lstm_model.keras")