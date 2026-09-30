import sys
import csv
import time

sys.path.append("C:/Users/HP/agri-proj")

import tensorflow as tf
from encryption import ModelEncryptor


print("Loading actual FL global model...")

model = tf.keras.models.load_model(
    "person3_federated/global_model.keras"
)

weights = model.get_weights()

print("FL model loaded successfully.")
print("Number of weight arrays:", len(weights))


security = ModelEncryptor()


# -----------------------------
# SECURITY INTEGRATION
# -----------------------------

print("\nStarting security integration test...")

# Encryption
encrypted_data, nonce, encryption_time, original_size = \
    security.encrypt_weights(weights)

encrypted_size = len(encrypted_data)


# Decryption
decrypted_weights, decryption_time, decrypted_size = \
    security.decrypt_weights(
        encrypted_data,
        nonce
    )


# Verify original and decrypted weights
weights_match = all(
    (original == decrypted).all()
    for original, decrypted in zip(
        weights,
        decrypted_weights
    )
)


# Convert times to milliseconds
encryption_time_ms = encryption_time * 1000
decryption_time_ms = decryption_time * 1000

total_security_time_ms = (
    encryption_time_ms +
    decryption_time_ms
)

payload_overhead = (
    encrypted_size -
    original_size
)

payload_overhead_percent = (
    payload_overhead /
    original_size
) * 100


# -----------------------------
# DISPLAY RESULTS
# -----------------------------

print("\n========== SECURITY INTEGRATION ==========")

print("Original payload:", original_size, "bytes")
print("Encrypted payload:", encrypted_size, "bytes")

print(
    "Payload overhead:",
    payload_overhead,
    "bytes"
)

print(
    "Payload overhead:",
    f"{payload_overhead_percent:.6f}%"
)

print(
    "Encryption time:",
    f"{encryption_time_ms:.6f} ms"
)

print(
    "Decryption time:",
    f"{decryption_time_ms:.6f} ms"
)

print(
    "Total security processing time:",
    f"{total_security_time_ms:.6f} ms"
)

if weights_match:
    print("Weight verification: SUCCESS")
else:
    print("Weight verification: FAILED")


# -----------------------------
# SAVE INTEGRATION RESULT
# -----------------------------

with open(
    "person6-baseline-security-integration/security_integration_results.csv",
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
        "encryption_time_ms",
        encryption_time_ms
    ])

    writer.writerow([
        "decryption_time_ms",
        decryption_time_ms
    ])

    writer.writerow([
        "total_security_processing_time_ms",
        total_security_time_ms
    ])

    writer.writerow([
        "weights_verified",
        weights_match
    ])


print("\nIntegration results saved to:")
print(
    "person6-baseline-security-integration/"
    "security_integration_results.csv"
)