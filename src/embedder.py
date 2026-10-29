import cv2
import numpy as np

class Embedder:
    def __init__(self):
        pass

    def embed(self, image, bit_stream):
        stego = image.copy()

        bit_index = 0
        total_bits = len(bit_stream)

        height, width, channels = stego.shape

        for row in range(height):
            for col in range(width):
                for channel in range(channels):
                    if bit_index >= total_bits:
                        return stego
                    
                    pixel = stego[row, col, channel]

                    bit = int(bit_stream[bit_index])

                    pixel = (pixel & 0xFE) | bit

                    stego[row, col, channel] = pixel

                    bit_index += 1
        
        raise ValueError("Message is too large for this image")
    
    def extract(self, image, num_bits):
        bits = []

        height, width, channels = image.shape

        bit_count = 0

        for row in range(height):
            for col in range(width):
                for channel in range(channels):
                    if bit_count >= num_bits:
                        return ''.join(bits)
                    
                    pixel = image[row, col, channel]

                    bits.append(str(pixel & 1))

                    bit_count += 1
        
        return ''.join(bits)