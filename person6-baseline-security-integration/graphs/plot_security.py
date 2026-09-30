import matplotlib.pyplot as plt
import os

# Measured security results from the actual FL model test
encryption_time = 0.1125
decryption_time = 0.0465

labels = ["Encryption", "Decryption"]
times = [encryption_time, decryption_time]

plt.figure(figsize=(8, 5))
plt.bar(labels, times)

plt.title("Encryption vs Decryption Time")
plt.xlabel("Security Operation")
plt.ylabel("Time (ms)")

for i, value in enumerate(times):
    plt.text(i, value + 0.002, f"{value:.4f} ms",
             ha="center")

plt.tight_layout()

output_path = os.path.join(
    os.path.dirname(__file__),
    "encryption_decryption_time.png"
)

plt.savefig(output_path, dpi=300)
plt.close()

print("Security graph saved to:")
print(output_path)