"""
Federated LSTM training with weighted FedAvg (4 clients).

Run from the repository root:
    python person3_federated/federated_training.py
"""
import os

import pandas as pd
import tensorflow as tf

from client import FLClient
from server import FLServer


# -----------------------------
# 1. Configuration
# -----------------------------

NUM_CLIENTS = 4
NUM_ROUNDS = 20
LOCAL_EPOCHS = 5
BATCH_SIZE = 32
SEED = 42

RESULTS_DIR = "person3_federated"
MODEL_PATH = f"{RESULTS_DIR}/global_model.keras"
RESULTS_PATH = f"{RESULTS_DIR}/fl_results.csv"

tf.keras.utils.set_random_seed(SEED)


# -----------------------------
# 2. Create server and clients
# -----------------------------

server = FLServer()
clients = [FLClient(k) for k in range(1, NUM_CLIENTS + 1)]

for c in clients:
    print(f"Client {c.client_id}: X {c.X.shape}, y {c.y.shape}")
print(f"Total samples: {sum(c.num_samples for c in clients)}")
print(f"X_test: {server.X_test.shape}")


# -----------------------------
# 3. Federated training loop
# -----------------------------

results = []

for rnd in range(1, NUM_ROUNDS + 1):
    global_weights = server.get_weights()

    client_weights = []
    client_sizes = []

    for c in clients:
        weights, n_k, loss = c.fit(global_weights, LOCAL_EPOCHS, BATCH_SIZE)
        client_weights.append(weights)
        client_sizes.append(n_k)
        print(f"  Round {rnd} | Client {c.client_id} | n={n_k} | local loss={loss:.2f}")

    server.aggregate(client_weights, client_sizes)

    metrics = server.evaluate()
    results.append({"round": rnd, **metrics})

    print(
        f"Round {rnd:2d} | MAE {metrics['mae']:.4f} | MSE {metrics['mse']:.4f} | "
        f"RMSE {metrics['rmse']:.4f} | R² {metrics['r2']:.4f}"
    )


# -----------------------------
# 4. Save results and model
# -----------------------------

pd.DataFrame(results).to_csv(RESULTS_PATH, index=False)
server.save(MODEL_PATH)

print("\nResults saved to:", RESULTS_PATH)
print("Global model saved to:", MODEL_PATH)
