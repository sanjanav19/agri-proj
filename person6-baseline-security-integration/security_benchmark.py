import sys
import csv
import statistics

sys.path.append("C:/Users/HP/agri-proj")

import tensorflow as tf
from encryption import ModelEncryptor


# Load the actual FL global model
model = tf.keras.models.load_model(
    "person3_federated/global_model.keras"
)

weights = model.get_weights()

security = ModelEncryptor()

RUNS = 10

encryption_times = []
decryption_times = []

original_size = None
encrypted_size = None

print("Starting security benchmark...")
print("Runs:", RUNS)
print()

for i in range(RUNS):

    encrypted_data, nonce, encryption_time, original_size = \
        security.encrypt_weights(weights)

    decrypted_weights, decryption_time, decrypted_size = \
        security.decrypt_weights(
            encrypted_data,
            nonce
        )

    encryption_times.append(encryption_time * 1000)
    decryption_times.append(decryption_time * 1000)

    encrypted_size = len(encrypted_data)

    # Verify weights
    success = all(
        (original == decrypted).all()
        for original, decrypted in zip(weights, decrypted_weights)
    )

    print(
        f"Run {i + 1}: "
        f"Encryption = {encryption_times[-1]:.6f} ms, "
        f"Decryption = {decryption_times[-1]:.6f} ms, "
        f"Status = {'SUCCESS' if success else 'ERROR'}"
    )


# Calculate averages
avg_encryption = statistics.mean(encryption_times)
avg_decryption = statistics.mean(decryption_times)

min_encryption = min(encryption_times)
max_encryption = max(encryption_times)

min_decryption = min(decryption_times)
max_decryption = max(decryption_times)

payload_overhead = encrypted_size - original_size

payload_overhead_percent = (
    payload_overhead / original_size
) * 100


print("\n========== SECURITY BENCHMARK RESULTS ==========")

print(f"Original payload size: {original_size} bytes")
print(f"Encrypted payload size: {encrypted_size} bytes")
print(f"Payload overhead: {payload_overhead} bytes")
print(f"Payload overhead percentage: {payload_overhead_percent:.6f}%")

print(f"\nAverage encryption time: {avg_encryption:.6f} ms")
print(f"Minimum encryption time: {min_encryption:.6f} ms")
print(f"Maximum encryption time: {max_encryption:.6f} ms")

print(f"\nAverage decryption time: {avg_decryption:.6f} ms")
print(f"Minimum decryption time: {min_decryption:.6f} ms")
print(f"Maximum decryption time: {max_decryption:.6f} ms")


# Save results
with open(
    "person6-baseline-security-integration/security_benchmark.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "metric",
        "value"
    ])

    writer.writerow([
        "original_payload_bytes",
        original_size
    ])

    writer.writerow([
        "encrypted_payload_bytes",
        encrypted_size
    ])

    writer.writerow([
        "payload_overhead_bytes",
        payload_overhead
    ])

    writer.writerow([
        "payload_overhead_percent",
        payload_overhead_percent
    ])

    writer.writerow([
        "average_encryption_time_ms",
        avg_encryption
    ])

    writer.writerow([
        "min_encryption_time_ms",
        min_encryption
    ])

    writer.writerow([
        "max_encryption_time_ms",
        max_encryption
    ])

    writer.writerow([
        "average_decryption_time_ms",
        avg_decryption
    ])

    writer.writerow([
        "min_decryption_time_ms",
        min_decryption
    ])

    writer.writerow([
        "max_decryption_time_ms",
        max_decryption
    ])

print("\nResults saved to:")
print("person6-baseline-security-integration/security_benchmark.csv")