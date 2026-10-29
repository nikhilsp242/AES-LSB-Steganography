import cv2
import numpy as np

a = cv2.imread("results/stego/baboon_512_500B.png")
b = cv2.imread("results/modified_stego/baboon_512_500B.png")

print("Images identical:", np.array_equal(a, b))

diff_pixels = np.sum(np.any(a != b, axis=2))

print("Different pixels:", diff_pixels)
print("Total pixels:", a.shape[0] * a.shape[1])
print("NPCR:", diff_pixels / (a.shape[0] * a.shape[1]) * 100)