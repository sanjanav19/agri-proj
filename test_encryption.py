from encryption import ModelEncryptor

fake_weights = [
    [[1.0, 2.0], [3.0, 4.0]],
    [5.0, 6.0]
]

security = ModelEncryptor()

encrypted_data, nonce, encryption_time, original_size = \
    security.encrypt_weights(fake_weights)

print("Original size:", original_size, "bytes")
print("Encrypted size:", len(encrypted_data), "bytes")
print("Encryption time:", encryption_time * 1000, "ms")

decrypted_weights, decryption_time, decrypted_size = \
    security.decrypt_weights(encrypted_data, nonce)

print("Decryption time:", decryption_time * 1000, "ms")

if fake_weights == decrypted_weights:
    print("SUCCESS: Original and decrypted weights are identical!")
else:
    print("ERROR: Weights are different!")