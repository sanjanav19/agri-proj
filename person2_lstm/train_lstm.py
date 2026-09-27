import os
import pandas as pd
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from lstm_model import create_lstm_model


# -----------------------------
# 1. Paths
# -----------------------------

DATA_DIR = "processed"
MODEL_DIR = "models"
RESULTS_DIR = "person2_lstm/results"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


# -----------------------------
# 2. Load processed data
# -----------------------------

X_train = pd.read_csv(f"{DATA_DIR}/X_train.csv").values
X_val = pd.read_csv(f"{DATA_DIR}/X_val.csv").values
X_test = pd.read_csv(f"{DATA_DIR}/X_test.csv").values

y_train = pd.read_csv(f"{DATA_DIR}/y_train.csv").values
y_val = pd.read_csv(f"{DATA_DIR}/y_val.csv").values
y_test = pd.read_csv(f"{DATA_DIR}/y_test.csv").values


# -----------------------------
# 3. Convert to NumPy
# -----------------------------

X_train = np.asarray(X_train, dtype=np.float32)
X_val = np.asarray(X_val, dtype=np.float32)
X_test = np.asarray(X_test, dtype=np.float32)

y_train = np.asarray(y_train, dtype=np.float32).ravel()
y_val = np.asarray(y_val, dtype=np.float32).ravel()
y_test = np.asarray(y_test, dtype=np.float32).ravel()


# -----------------------------
# 4. Reshape for LSTM
# -----------------------------
# Current:
# (samples, 38)
#
# LSTM requires:
# (samples, timesteps, features)
#
# We use one timestep containing 38 features.

X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
X_val = X_val.reshape(X_val.shape[0], 1, X_val.shape[1])
X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])


print("X_train:", X_train.shape)
print("X_val:", X_val.shape)
print("X_test:", X_test.shape)


# -----------------------------
# 5. Create model
# -----------------------------

model = create_lstm_model(
    input_shape=(1, X_train.shape[2])
)

model.summary()


# -----------------------------
# 6. Train model
# -----------------------------

# -----------------------------
# 6. Train model
# -----------------------------

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    f"{MODEL_DIR}/lstm_model.keras",
    monitor="val_loss",
    save_best_only=True
)

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=100,
    batch_size=32,
    callbacks=[early_stopping, checkpoint],
    verbose=1
)


# -----------------------------
# 7. Model already saved by checkpoint
# -----------------------------

print("\nBest model saved successfully!")


# -----------------------------
# 8. Save training history
# -----------------------------

history_df = pd.DataFrame(history.history)

history_df.to_csv(
    f"{RESULTS_DIR}/training_history.csv",
    index=False
)

print("Training history saved!")