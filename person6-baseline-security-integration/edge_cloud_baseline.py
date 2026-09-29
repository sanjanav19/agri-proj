import os
import sys
import numpy as np
import pandas as pd

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

DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "processed"
)

RESULTS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "edge_cloud_results"
)

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
# 3. Experimental configuration
# --------------------------------------------------

NUM_CLIENTS = 4
NUM_ROUNDS = 20
LOCAL_EPOCHS = 5
BATCH_SIZE = 32
SEED = 42

tf_seed = SEED
np.random.seed(tf_seed)

# --------------------------------------------------
# 4. Load edge-client datasets
# --------------------------------------------------

clients = []

for client_id in range(1, NUM_CLIENTS + 1):

    client_dir = os.path.join(
        DATA_DIR,
        f"client_{client_id}"
    )

    X = np.load(
        os.path.join(client_dir, "X.npy")
    ).astype("float32")

    y = np.load(
        os.path.join(client_dir, "y.npy")
    ).astype("float32")

    X = X.reshape(
        X.shape[0],
        1,
        X.shape[1]
    )

    clients.append((X, y))

    print(
        f"Client {client_id}: "
        f"X={X.shape}, y={y.shape}"
    )

# --------------------------------------------------
# 5. Create cloud model
# --------------------------------------------------

cloud_model = create_lstm_model(
    input_shape=(1, 38)
)

print("\nCloud model:")
cloud_model.summary()

# --------------------------------------------------
# 6. Edge-Cloud training
# --------------------------------------------------

print("\nStarting Edge-Cloud LSTM training...")

for rnd in range(1, NUM_ROUNDS + 1):

    print(
        f"\n========== Round {rnd}/{NUM_ROUNDS} =========="
    )

    global_weights = cloud_model.get_weights()

    client_weights = []
    client_sizes = []

    # --------------------------------------------------
    # Edge-side local training
    # --------------------------------------------------

    for client_id, (X_client, y_client) in enumerate(
        clients,
        start=1
    ):

        print(
            f"Training Edge Client {client_id}..."
        )

        edge_model = create_lstm_model(
            input_shape=(1, 38)
        )

        edge_model.set_weights(
            global_weights
        )

        edge_model.fit(
            X_client,
            y_client,
            epochs=LOCAL_EPOCHS,
            batch_size=BATCH_SIZE,
            verbose=0
        )

        client_weights.append(
            edge_model.get_weights()
        )

        client_sizes.append(
            len(y_client)
        )

    # --------------------------------------------------
    # Cloud-side weighted aggregation
    # --------------------------------------------------

    total_samples = sum(client_sizes)

    aggregated_weights = []

    for layer_weights in zip(*client_weights):

        weighted_layer = sum(
            weights * (n / total_samples)
            for weights, n in zip(
                layer_weights,
                client_sizes
            )
        )

        aggregated_weights.append(
            weighted_layer
        )

    cloud_model.set_weights(
        aggregated_weights
    )

    print(
        f"Round {rnd} cloud aggregation completed."
    )

# --------------------------------------------------
# 7. Load centralized test set
# --------------------------------------------------

X_test = pd.read_csv(
    os.path.join(DATA_DIR, "X_test.csv")
).values.astype("float32")

y_test = pd.read_csv(
    os.path.join(DATA_DIR, "y_test.csv")
).values.astype("float32").ravel()

X_test = X_test.reshape(
    X_test.shape[0],
    1,
    X_test.shape[1]
)

print("\nTest set:")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)

# --------------------------------------------------
# 8. Evaluate cloud model
# --------------------------------------------------

print("\nEvaluating Edge-Cloud model...")

y_pred = cloud_model.predict(
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
# 9. Display results
# --------------------------------------------------

print("\n========================================")
print("EDGE-CLOUD LSTM RESULTS")
print("========================================")
print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R2   : {r2:.4f}")
print("========================================")

# --------------------------------------------------
# 10. Save metrics
# --------------------------------------------------

metrics = pd.DataFrame([
    {
        "model": "Edge-Cloud LSTM",
        "mae": mae,
        "mse": mse,
        "rmse": rmse,
        "r2": r2,
        "clients": NUM_CLIENTS,
        "rounds": NUM_ROUNDS,
        "local_epochs": LOCAL_EPOCHS,
        "batch_size": BATCH_SIZE,
        "seed": SEED
    }
])

metrics.to_csv(
    os.path.join(
        RESULTS_DIR,
        "edge_cloud_metrics.csv"
    ),
    index=False
)

# --------------------------------------------------
# 11. Save predictions
# --------------------------------------------------

predictions = pd.DataFrame({
    "actual": y_test,
    "predicted": y_pred
})

predictions.to_csv(
    os.path.join(
        RESULTS_DIR,
        "edge_cloud_predictions.csv"
    ),
    index=False
)

# --------------------------------------------------
# 12. Save cloud model
# --------------------------------------------------

cloud_model.save(
    os.path.join(
        RESULTS_DIR,
        "edge_cloud_lstm_model.keras"
    )
)

print("\nResults saved.")