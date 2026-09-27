import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Reuse Person 2's model factory
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "person2_lstm")
)
from lstm_model import create_lstm_model

from fedavg import fedavg


DATA_DIR = "processed"
NUM_FEATURES = 38


class FLServer:
    """Holds the global model, aggregates client updates, evaluates on the test set."""

    def __init__(self):
        self.global_model = create_lstm_model(input_shape=(1, NUM_FEATURES))

        # Centralized test set (never used for training)
        X_test = pd.read_csv(f"{DATA_DIR}/X_test.csv").values.astype("float32")
        y_test = pd.read_csv(f"{DATA_DIR}/y_test.csv").values.astype("float32").ravel()

        self.X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])
        self.y_test = y_test

    def get_weights(self):
        return self.global_model.get_weights()

    def aggregate(self, client_weights, client_sizes):
        new_weights = fedavg(client_weights, client_sizes)
        self.global_model.set_weights(new_weights)

    def evaluate(self):
        y_pred = self.global_model.predict(self.X_test, verbose=0).ravel()

        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, y_pred)

        return {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}

    def save(self, path):
        self.global_model.save(path)
