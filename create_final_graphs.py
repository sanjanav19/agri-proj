import csv
import matplotlib.pyplot as plt

# Read final comparison
names = []
mae = []
rmse = []
energy = []

with open("final_results/final_comparison.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        names.append(row["Approach"])
        mae.append(float(row["MAE"]))
        rmse.append(float(row["RMSE"]))
        energy.append(float(row["Energy_J"]))

# MAE
plt.figure(figsize=(9, 5))
plt.bar(names, mae)
plt.ylabel("MAE")
plt.title("MAE Comparison")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("final_results/mae_comparison.png", dpi=200)
plt.close()

# RMSE
plt.figure(figsize=(9, 5))
plt.bar(names, rmse)
plt.ylabel("RMSE")
plt.title("RMSE Comparison")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("final_results/rmse_comparison.png", dpi=200)
plt.close()

# Energy
plt.figure(figsize=(9, 5))
plt.bar(names, energy)
plt.ylabel("Energy (J)")
plt.title("Energy Consumption Comparison")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("final_results/energy_comparison.png", dpi=200)
plt.close()

print("FINAL GRAPHS CREATED")