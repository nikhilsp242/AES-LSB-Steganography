# AES-256 in CBC mode with PKCS7 padding
# It's a standard, secure configuration.
# The paper mentions AES-256 as an example.
# Python's cryptography library provides a robust implementation.
import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AES256:

    def __init__(self, key: bytes):
        """
        AES-256 requires a 32-byte (256-bit) key.
        """
        if len(key) != 32:
            raise ValueError("AES-256 key must be exactly 32 bytes.")

        self.key = key

    def encrypt_with_iv(self, plaintext: str, iv: bytes):

        plaintext = plaintext.encode("utf-8")

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv)
        )

        encryptor = cipher.encryptor()

        ciphertext = (
            encryptor.update(padded_data)
            + encryptor.finalize()
        )

        return ciphertext

    def encrypt(self, plaintext: str):
        """
        Encrypt a plaintext string.

        Returns:
            iv (bytes)
            ciphertext (bytes)
        """

        plaintext = plaintext.encode("utf-8")

        # PKCS7 Padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        # Random IV
        iv = os.urandom(16)

        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv)
        )

        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return iv, ciphertext

    def decrypt(self, iv: bytes, ciphertext: bytes):
        """
        Decrypt ciphertext.

        Returns:
            plaintext (str)
        """

        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv)
        )

        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()

        plaintext = unpadder.update(padded_plaintext)
        plaintext += unpadder.finalize()

        return plaintext.decode("utf-8")
