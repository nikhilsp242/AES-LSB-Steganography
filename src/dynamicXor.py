class DynamicXOR:
    def __init__(self):
        pass
    
    def xor_message(self, binary_message: str, dynamic_key: str):
        embedded_bits = ''.join(
            str(int(message_bit) ^ int(key_bit))
            for message_bit, key_bit in zip(binary_message, dynamic_key)
        )
        return embedded_bits
    
    def recover_message(self, embedded_bits: str, dynamic_key: str):
        binary_message = ''.join(
            str(int(bit) ^ int(key))
            for bit, key in zip(embedded_bits, dynamic_key)
        )
        return binary_message