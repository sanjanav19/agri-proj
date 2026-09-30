import time
import numpy as np
import pandas as pd
import os

ROUNDS = 20


results = []

print("====================================")
print("LATENCY MEASUREMENT")
print("====================================")

for round_number in range(1, ROUNDS + 1):



    start_time = time.perf_counter()


    data = np.random.rand(1000, 1000)
    result = np.dot(data, data)

    end_time = time.perf_counter()

    computation_latency = (
        end_time - start_time
    ) * 1000



    start_time = time.perf_counter()

    # Simulate sending/receiving data
    message = data.tobytes()

    # Convert received data back
    received = np.frombuffer(
        message,
        dtype=data.dtype
    )

    end_time = time.perf_counter()

    communication_latency = (
        end_time - start_time
    ) * 1000



    total_latency = (
        computation_latency +
        communication_latency
    )


    results.append({
        "Round": round_number,
        "Computation Latency (ms)": computation_latency,
        "Communication Latency (ms)": communication_latency,
        "Total Latency (ms)": total_latency
    })


    print(
        f"Round {round_number}: "
        f"Computation = {computation_latency:.4f} ms, "
        f"Communication = {communication_latency:.4f} ms, "
        f"Total = {total_latency:.4f} ms"
    )




df = pd.DataFrame(results)

print("\n====================================")
print("LATENCY RESULTS")
print("====================================")

print(df)


# --------------------------------
# Save results
# --------------------------------

os.makedirs("results", exist_ok=True)

df.to_csv(
    "results/latency_results.csv",
    index=False
)

print("\nResults saved to:")
print("results/latency_results.csv")


# --------------------------------
# Average latency
# --------------------------------

average_computation = df[
    "Computation Latency (ms)"
].mean()

average_communication = df[
    "Communication Latency (ms)"
].mean()

average_total = df[
    "Total Latency (ms)"
].mean()


print("\n====================================")
print("AVERAGE LATENCY")
print("====================================")

print(
    f"Average Computation Latency: "
    f"{average_computation:.4f} ms"
)

print(
    f"Average Communication Latency: "
    f"{average_communication:.4f} ms"
)

print(
    f"Average Total Latency: "
    f"{average_total:.4f} ms"
)