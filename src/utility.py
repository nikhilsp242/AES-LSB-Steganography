class Utility:
    def __init__(self):
        pass

    def message_to_binary(self, message):
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        return binary_message
    
    def binary_to_message(self, binary):
        message = ""

        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            message += chr(int(byte, 2))
        return message
    
    def bytes_to_binary(self, data: bytes):
        return ''.join(format(byte, '08b') for byte in data)
    
    def binary_to_bytes(self, binary):
        return bytes(
            int(binary[i:i+8], 2)
            for i in range(0, len(binary), 8)
        )
    
    def generate_dynamic_key(self, binary_message):
        key = ""

        for i in range(len(binary_message)):
            key += str(i%2)
        return key
    
    
