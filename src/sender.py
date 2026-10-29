import cv2


class Sender:

    def __init__(self, aes, utility, dxor, embedder):
        self.aes = aes
        self.utility = utility
        self.dxor = dxor
        self.embedder = embedder

    def embed_message(self, image, message):

        # AES encryption
        iv, ciphertext = self.aes.encrypt(message)

        # Ciphertext → binary
        binary_ciphertext = self.utility.bytes_to_binary(ciphertext)

        # Generate dynamic key
        dynamic_key = self.utility.generate_dynamic_key(
            binary_ciphertext
        )

        # Dynamic XOR
        embedded_bits = self.dxor.xor_message(
            binary_ciphertext,
            dynamic_key
        )

        # Embed into image
        stego = self.embedder.embed(
            image.copy(),
            embedded_bits
        )

        return stego, iv, dynamic_key, len(embedded_bits)