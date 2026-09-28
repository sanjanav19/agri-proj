import time
import pandas as pd
from contextlib import contextmanager

class LatencyLogger:
    def __init__(self):
        self.records = []

    @contextmanager
    def measure(self, round_id, component, client_id=None):
        start = time.perf_counter()
        yield
        elapsed_ms = (time.perf_counter() - start) * 1000
        self.records.append({
            "round": round_id,
            "component": component,
            "client": client_id,
            "latency_ms": elapsed_ms,
        })

    def save(self, path="latency/results/latency_results.csv"):
        pd.DataFrame(self.records).to_csv(path, index=False)

if __name__ == "__main__":
    logger = LatencyLogger()
    with logger.measure(round_id=1, component="test_sleep"):
        time.sleep(0.5)
    print(logger.records)