import pickle
import os
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class ModelEncryptor:

    def __init__(self):
        self.key = AESGCM.generate_key(bit_length=256)
        self.aes = AESGCM(self.key)

    def serialize_weights(self, weights):
        return pickle.dumps(weights)

    def deserialize_weights(self, data):
        return pickle.loads(data)

    def encrypt_weights(self, weights):
        data = self.serialize_weights(weights)

        nonce = os.urandom(12)

        start = time.perf_counter()

        encrypted_data = self.aes.encrypt(
            nonce,
            data,
            None
        )

        encryption_time = time.perf_counter() - start

        return encrypted_data, nonce, encryption_time, len(data)

    def decrypt_weights(self, encrypted_data, nonce):

        start = time.perf_counter()

        decrypted_data = self.aes.decrypt(
            nonce,
            encrypted_data,
            None
        )

        decryption_time = time.perf_counter() - start

        weights = self.deserialize_weights(decrypted_data)

        return weights, decryption_time, len(decrypted_data)