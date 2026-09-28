
import os
import pickle
import sys

import pandas as pd
import tensorflow as tf

sys.path.insert(0, "person3_federated")   # so "from client import ..." works
from client import FLClient               # noqa: E402
from server import FLServer               # noqa: E402
from latency_measurement import LatencyLogger  # noqa: E402

# ---- MUST match person3_federated/federated_training.py ----
NUM_CLIENTS = 4
LOCAL_EPOCHS = 5
BATCH_SIZE = 32
SEED = 42
# ------------------------------------------------------------
NUM_TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
NUM_ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 20
BANDWIDTH_MBPS = 10   # assumed link speed. Write this in your methodology.

OUT_DIR = "latency/results"


def transfer(logger, rnd, component, weights, client_id):
    """Real serialize + deserialize time, plus a simulated network delay."""
    with logger.measure(rnd, component, client_id):
        data = pickle.dumps(weights)
        weights = pickle.loads(data)
    link_ms = len(data) * 8 / (BANDWIDTH_MBPS * 1e6) * 1000
    logger.records.append({"round": rnd, "component": component + "_link",
                           "client": client_id, "latency_ms": link_ms})
    return weights, len(data)


def run_trial(trial):
    tf.keras.utils.set_random_seed(SEED)
    logger = LatencyLogger()
    accuracy, payloads = [], []

    server = FLServer()
    clients = [FLClient(k) for k in range(1, NUM_CLIENTS + 1)]

    for rnd in range(1, NUM_ROUNDS + 1):
        with logger.measure(rnd, "total_round"):
            global_weights = server.get_weights()
            client_weights, client_sizes = [], []

            for c in clients:
                # server -> client
                w, _ = transfer(logger, rnd, "comm_server_to_client",
                                global_weights, c.client_id)
                # local training
                with logger.measure(rnd, "local_training", c.client_id):
                    w, n_k, _loss = c.fit(w, LOCAL_EPOCHS, BATCH_SIZE)
                # client -> server
                # (encryption would go here later: time "encryption" before
                #  transfer and "decryption" after it)
                w, nbytes = transfer(logger, rnd, "comm_client_to_server",
                                     w, c.client_id)
                client_weights.append(w)
                client_sizes.append(n_k)
                payloads.append({"trial": trial, "round": rnd,
                                 "client": c.client_id, "payload_bytes": nbytes})

            # FedAvg (server.aggregate)
            with logger.measure(rnd, "fedavg"):
                server.aggregate(client_weights, client_sizes)

        # evaluation is OUTSIDE the timers
        m = server.evaluate()
        accuracy.append({"trial": trial, "round": rnd, **m})
        print(f"trial {trial} round {rnd:2d} | RMSE {m['rmse']:.4f}")

    lat = pd.DataFrame(logger.records)
    lat.insert(0, "trial", trial)
    return lat, pd.DataFrame(accuracy), pd.DataFrame(payloads)


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    lats, accs, pays = [], [], []
    for t in range(1, NUM_TRIALS + 1):
        print(f"=== Trial {t}/{NUM_TRIALS} ===")
        l, a, p = run_trial(t)
        lats.append(l); accs.append(a); pays.append(p)

    pd.concat(lats).to_csv(f"{OUT_DIR}/latency_results.csv", index=False)
    pd.concat(accs).to_csv(f"{OUT_DIR}/accuracy_check.csv", index=False)
    pd.concat(pays).to_csv(f"{OUT_DIR}/payload_sizes.csv", index=False)
    print(f"Saved 3 CSV files in {OUT_DIR}")