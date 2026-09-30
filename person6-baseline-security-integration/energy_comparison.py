import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("results", exist_ok=True)

data = {
    "Model": [
        "Federated / FLyer",
        "Edge-Cloud",
        "Cloud"
    ],

    "Minimum Energy (KJ)": [
        4,
        8,
        12
    ],

    "Maximum Energy (KJ)": [
        6,
        10,
        14
    ]
}

df = pd.DataFrame(data)

df["Average Energy (KJ)"] = (
    df["Minimum Energy (KJ)"] +
    df["Maximum Energy (KJ)"]
) / 2

print("======================================")
print("ENERGY COMPARISON")
print("======================================")

print(df.to_string(index=False))

df.to_csv(
    "results/energy_comparison.csv",
    index=False
)

print()
print("Energy comparison CSV saved.")


plt.figure(figsize=(8, 5))

plt.bar(
    df["Model"],
    df["Average Energy (KJ)"]
)

plt.title("Energy Consumption Comparison")
plt.xlabel("Architecture")
plt.ylabel("Energy Consumption (KJ)")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    "results/energy_comparison.png",
    dpi=300
)

plt.close()

print("Energy comparison graph saved.")

print()
print("======================================")
print("ENERGY COMPARISON COMPLETED")
print("======================================")