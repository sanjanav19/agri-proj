"""Make latency graphs from latency_results.csv.
Run from the project root:  python latency/plot_latency.py
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "latency/results/latency_results.csv"
OUT = "latency/results"


def save(name):
    plt.tight_layout()
    plt.savefig(f"{OUT}/{name}.png", dpi=300)
    plt.close()
    print("saved", name)


df = pd.read_csv(CSV)
os.makedirs(OUT, exist_ok=True)

# per-round mean of each component (averaged over clients)
per_round = df.groupby(["round", "component"])["latency_ms"].mean().unstack()


def comps(*names):
    return [n for n in names if n in per_round.columns]


# 1. total latency vs rounds
if "total_round" in per_round:
    per_round["total_round"].plot(marker="o")
    plt.xlabel("FL round"); plt.ylabel("Latency (ms)"); plt.title("Total round latency")
    save("latency_vs_rounds")

# 2. communication latency (real serialization + simulated link)
c = comps("comm_client_to_server", "comm_client_to_server_link",
          "comm_server_to_client", "comm_server_to_client_link")
if c:
    per_round[c].plot(marker="o")
    plt.xlabel("FL round"); plt.ylabel("Latency (ms)"); plt.title("Communication latency")
    save("communication_latency")

# 3. computation latency
c = comps("local_training", "fedavg")
if c:
    per_round[c].plot(marker="o")
    plt.xlabel("FL round"); plt.ylabel("Latency (ms)"); plt.title("Computation latency")
    save("computation_latency")

# 4. encryption latency (only if security module was used)
c = comps("encryption", "decryption")
if c:
    per_round[c].plot(marker="o")
    plt.xlabel("FL round"); plt.ylabel("Latency (ms)"); plt.title("Encryption latency")
    save("encryption_latency")

# 5. stacked breakdown. local training and comm happen per client, so sum over clients
summed = df[df["component"] != "total_round"].groupby(["round", "component"])["latency_ms"].sum().unstack()
summed.plot(kind="bar", stacked=True)
plt.xlabel("FL round"); plt.ylabel("Latency (ms)"); plt.title("Latency breakdown per round")
save("total_latency")