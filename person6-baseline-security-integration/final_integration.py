import csv
import os

# -----------------------------
# Existing security result
# -----------------------------
security_file = "person6-baseline-security-integration/security_integration_results.csv"

security = {}

with open(security_file, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) >= 2:
            security[row[0]] = row[1]


# -----------------------------
# Security values
# -----------------------------
original_payload = float(security["original_payload_bytes"])
encrypted_payload = float(security["encrypted_payload_bytes"])
encryption_time = float(security["encryption_time_ms"])
decryption_time = float(security["decryption_time_ms"])

security_processing_time = encryption_time + decryption_time

payload_overhead = encrypted_payload - original_payload
payload_overhead_percent = (payload_overhead / original_payload) * 100


# -----------------------------
# Federated latency values
# From the completed latency run
# -----------------------------
# 20 rounds × 4 clients
NUM_ROUNDS = 20
NUM_CLIENTS = 4

# Your measured communication link latency
link_latency_ms = 137.9184

# Security overhead is applied to the model/weight transmission
# for each client communication direction.
security_overhead_per_round = (
    security_processing_time * NUM_CLIENTS * 2
)

# Total security processing across 20 FL rounds
total_security_processing = (
    security_overhead_per_round * NUM_ROUNDS
)


# -----------------------------
# Save final integration data
# -----------------------------
output_file = (
    "person6-baseline-security-integration/"
    "final_integration_results.csv"
)

with open(output_file, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "metric",
        "value",
        "unit"
    ])

    writer.writerow([
        "num_clients",
        NUM_CLIENTS,
        "clients"
    ])

    writer.writerow([
        "num_rounds",
        NUM_ROUNDS,
        "rounds"
    ])

    writer.writerow([
        "communication_link_latency",
        link_latency_ms,
        "ms"
    ])

    writer.writerow([
        "original_payload",
        original_payload,
        "bytes"
    ])

    writer.writerow([
        "encrypted_payload",
        encrypted_payload,
        "bytes"
    ])

    writer.writerow([
        "payload_overhead",
        payload_overhead,
        "bytes"
    ])

    writer.writerow([
        "payload_overhead_percent",
        payload_overhead_percent,
        "%"
    ])

    writer.writerow([
        "encryption_time",
        encryption_time,
        "ms"
    ])

    writer.writerow([
        "decryption_time",
        decryption_time,
        "ms"
    ])

    writer.writerow([
        "security_processing_per_transmission",
        security_processing_time,
        "ms"
    ])

    writer.writerow([
        "security_processing_per_round",
        security_overhead_per_round,
        "ms"
    ])

    writer.writerow([
        "total_security_processing_20_rounds",
        total_security_processing,
        "ms"
    ])


# -----------------------------
# Display results
# -----------------------------
print("\n========== FINAL INTEGRATION ==========")

print("Clients:", NUM_CLIENTS)
print("FL rounds:", NUM_ROUNDS)

print("\n--- Communication ---")
print("Link latency:", link_latency_ms, "ms")

print("\n--- Security ---")
print("Original payload:", original_payload, "bytes")
print("Encrypted payload:", encrypted_payload, "bytes")
print("Payload overhead:", payload_overhead, "bytes")
print("Payload overhead:", payload_overhead_percent, "%")

print("\nEncryption time:", encryption_time, "ms")
print("Decryption time:", decryption_time, "ms")
print(
    "Security processing per transmission:",
    security_processing_time,
    "ms"
)

print(
    "Security processing per round:",
    security_overhead_per_round,
    "ms"
)

print(
    "Security processing over 20 rounds:",
    total_security_processing,
    "ms"
)

print("\nSaved to:")
print(output_file)