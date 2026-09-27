import os
import sys

import numpy as np

# Reuse Person 2's model factory
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "person2_lstm")
)
from lstm_model import create_lstm_model


DATA_DIR = "processed"


class FLClient:
    """One federated client: holds only its own local data."""

    def __init__(self, client_id):
        self.client_id = client_id

        X = np.load(f"{DATA_DIR}/client_{client_id}/X.npy").astype("float32")
        y = np.load(f"{DATA_DIR}/client_{client_id}/y.npy").astype("float32").ravel()

        # Same as Person 2: one timestep containing 38 features
        # (samples, 38) -> (samples, 1, 38)
        self.X = X.reshape(X.shape[0], 1, X.shape[1])
        self.y = y

        self.num_samples = self.X.shape[0]

    def fit(self, global_weights, epochs, batch_size):
        """Train locally starting from the global weights."""
        # Fresh model (and fresh Adam state) each round; only weights are shared
        model = create_lstm_model(input_shape=(1, self.X.shape[2]))
        model.set_weights(global_weights)

        history = model.fit(
            self.X,
            self.y,
            epochs=epochs,
            batch_size=batch_size,
            shuffle=True,
            verbose=0
        )

        return model.get_weights(), self.num_samples, history.history["loss"][-1]
