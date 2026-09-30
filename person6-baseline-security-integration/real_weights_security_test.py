import sys
sys.path.append("C:/Users/HP/agri-proj")

import tensorflow as tf
from encryption import ModelEncryptor

model = tf.keras.models.load_model(
    "person3_federated/global_model.keras"
)

weights = model.get_weights()

security = ModelEncryptor()

encrypted_data, nonce, encryption_time, original_size = \
    security.encrypt_weights(weights)

print("Original size:", original_size, "bytes")
print("Encrypted size:", len(encrypted_data), "bytes")
print("Encryption time:", encryption_time * 1000, "ms")

decrypted_weights, decryption_time, decrypted_size = \
    security.decrypt_weights(encrypted_data, nonce)

print("Decryption time:", decryption_time * 1000, "ms")

if all(
    (original == decrypted).all()
    for original, decrypted in zip(weights, decrypted_weights)
):
    print("SUCCESS: Actual FL weights restored correctly!")
else:
    print("ERROR: Actual FL weights are different!")