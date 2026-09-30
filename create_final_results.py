import csv
import os

os.makedirs("final_results", exist_ok=True)

rows = [
    ["Centralized LSTM", 1131.135986328125, 1254.8337539291808, -0.06544995307922363, 243.6682820004],
    ["Edge-Cloud LSTM", 1131.724609375, 1250.8683483884306, -0.05872666835784912, 3232.8565890012],
    ["Federated LSTM (Round 20)", 1113.5677490234375, 1232.2274039315957, -0.027406692504882812, 1555.0708039992],
]

with open("final_results/final_comparison.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Approach", "MAE", "RMSE", "R2", "Energy_J"])
    writer.writerows(rows)

security = [
    ["Original payload", 172398, "bytes"],
    ["Encrypted payload", 172414, "bytes"],
    ["Payload overhead", 16, "bytes"],
    ["Payload overhead percent", 0.00928085012587153, "%"],
    ["Encryption time", 0.11250001261942089, "ms"],
    ["Decryption time", 0.04650000482797623, "ms"],
    ["Security processing per transmission", 0.1590000174473971, "ms"],
    ["Security processing per round", 1.272000139579177, "ms"],
    ["Security processing - 20 rounds", 25.440002791583538, "ms"],
]

with open("final_results/security_summary.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Metric", "Value", "Unit"])
    writer.writerows(security)

print("FINAL RESULTS CREATED")
print("final_results/final_comparison.csv")
print("final_results/security_summary.csv")