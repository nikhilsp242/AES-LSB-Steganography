class Receiver:

    def __init__(self, aes, utility, dxor, embedder):
        self.aes = aes
        self.utility = utility
        self.dxor = dxor
        self.embedder = embedder

    def extract_message(
        self,
        stego,
        embedded_bits_length,
        dynamic_key,
        iv
    ):

        # Extract LSBs
        extracted_bits = self.embedder.extract(
            stego,
            embedded_bits_length
        )

        # Reverse Dynamic XOR
        recovered_bits = self.dxor.recover_message(
            extracted_bits,
            dynamic_key
        )

        # Binary → ciphertext
        ciphertext = self.utility.binary_to_bytes(
            recovered_bits
        )

        # AES decryption
        plaintext = self.aes.decrypt(
            iv,
            ciphertext
        )

        return plaintext