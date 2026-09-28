"""Fake FL loop (4 clients, random weights) to test the latency logger.
Run from the project root:  python latency/mock_fl.py
"""
import os
import pickle
import time
import random
import numpy as np
from latency_measurement import LatencyLogger

NUM_CLIENTS = 4
ROUNDS = 5
BANDWIDTH_MBPS = 10  # assumed link speed, write this in your methodology


def make_weights():
    return [np.random.rand(64, 128).astype("float32"),
            np.random.rand(128).astype("float32")]


def fake_local_train(weights):
    time.sleep(random.uniform(0.2, 0.4))  # pretend to train
    return [w + 0.01 * np.random.randn(*w.shape).astype("float32") for w in weights]


def fedavg(all_weights, sizes):
    total = sum(sizes)
    return [sum(n / total * w[i] for w, n in zip(all_weights, sizes))
            for i in range(len(all_weights[0]))]


def link_delay_ms(num_bytes):
    return num_bytes * 8 / (BANDWIDTH_MBPS * 1e6) * 1000


def transfer(logger, round_id, component, weights, client_id=None):
    """Real serialize/deserialize time + simulated network delay."""
    with logger.measure(round_id, component, client_id):
        data = pickle.dumps(weights)
        weights = pickle.loads(data)
    logger.records.append({"round": round_id, "component": component + "_link",
                           "client": client_id,
                           "latency_ms": link_delay_ms(len(data))})
    return weights, len(data)


if __name__ == "__main__":
    logger = LatencyLogger()
    global_weights = make_weights()
    sizes = [100, 150, 120, 130]  # fake sample counts per client

    for r in range(1, ROUNDS + 1):
        with logger.measure(r, "total_round"):
            received = []
            for c in range(NUM_CLIENTS):
                local, _ = transfer(logger, r, "comm_server_to_client", global_weights, c)
                with logger.measure(r, "local_training", c):
                    local = fake_local_train(local)
                local, nbytes = transfer(logger, r, "comm_client_to_server", local, c)
                received.append(local)
            with logger.measure(r, "fedavg"):
                global_weights = fedavg(received, sizes)
        print(f"Round {r} done, payload = {nbytes / 1024:.1f} KB")

    os.makedirs("latency/results", exist_ok=True)
    logger.save()
    print("Saved latency/results/latency_results.csv")