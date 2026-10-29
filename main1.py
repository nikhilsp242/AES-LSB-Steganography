import os
import csv
import cv2
import time

from src.aes import AES256
from src.utility import Utility
from src.dynamicXor import DynamicXOR
from src.embedder import Embedder
from src.metrics import Metrics

# --------------------------------------------------------
# Initialize
# --------------------------------------------------------

key = b"12345678901234567890123456789012"

aes = AES256(key)
utility = Utility()
dxor = DynamicXOR()
embedder = Embedder()
metrics = Metrics()

IMAGE_DIR = "data/images"
TEXT_DIR = "data/text"
STEGO_DIR = "results/stego"

os.makedirs(STEGO_DIR, exist_ok=True)
os.makedirs("results", exist_ok=True)

CSV_FILE = "results/metrics.csv"

# --------------------------------------------------------
# Create CSV
# --------------------------------------------------------

with open(CSV_FILE, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Image",
        "Resolution",
        "Payload",
        "Payload_Size(Bytes)",
        "AES_Encrypt_Time(s)",
        "Dynamic_XOR_Time(s)",
        "Embedding_Time(s)",
        "Sender_Total_Time(s)",
        "Extraction_Time(s)",
        "XOR_Recovery_Time(s)",
        "AES_Decrypt_Time(s)",
        "Receiver_Total_Time(s)",
        "PSNR",
        "MSE",
        "NPCR",
        "Entropy",
        "SSIM",
        "Q-Index"
    ])

    # ----------------------------------------------------
    # Loop over images
    # ----------------------------------------------------

    for image_name in sorted(os.listdir(IMAGE_DIR)):

        image_path = os.path.join(IMAGE_DIR, image_name)

        if not image_name.lower().endswith(
            (".png", ".jpg", ".jpeg", ".bmp", ".tiff")
        ):
            continue

        original = cv2.imread(image_path)

        height, width = original.shape[:2]
        resolution = f"{width}x{height}"

        # ------------------------------------------------
        # Loop over payloads
        # ------------------------------------------------

        for text_name in sorted(os.listdir(TEXT_DIR)):

            if not text_name.endswith(".txt"):
                continue

            text_path = os.path.join(TEXT_DIR, text_name)

            with open(text_path, "r", encoding="utf-8") as f:
                message = f.read()

            payload_size = len(message.encode("utf-8"))

            # ==================================================
            # Sender Side
            # ==================================================

            # AES Encryption
            aes_start = time.perf_counter()

            iv, ciphertext = aes.encrypt(message)

            aes_encrypt_time = time.perf_counter() - aes_start

            binary_ciphertext = utility.bytes_to_binary(ciphertext)

            # Dynamic XOR
            xor_start = time.perf_counter()

            dynamic_key = utility.generate_dynamic_key(binary_ciphertext)

            embedded_bits = dxor.xor_message(
                binary_ciphertext,
                dynamic_key
            )

            xor_time = time.perf_counter() - xor_start

            # Embedding
            embed_start = time.perf_counter()

            stego = embedder.embed(
                original.copy(),
                embedded_bits
            )

            embedding_time = time.perf_counter() - embed_start

            sender_total_time = (
                aes_encrypt_time
                + xor_time
                + embedding_time
            )

            # Save stego image
            stego_name = (
                f"{os.path.splitext(image_name)[0]}"
                f"_{os.path.splitext(text_name)[0]}.png"
            )

            stego_path = os.path.join(STEGO_DIR, stego_name)

            cv2.imwrite(stego_path, stego)

            # ==================================================
            # Receiver Side
            # ==================================================

            # Extraction
            extract_start = time.perf_counter()

            extracted_bits = embedder.extract(
                stego,
                len(embedded_bits)
            )

            extraction_time = (
                time.perf_counter() - extract_start
            )

            # XOR Recovery
            xor_recovery_start = time.perf_counter()

            recovered_bits = dxor.recover_message(
                extracted_bits,
                dynamic_key
            )

            restored_ciphertext = utility.binary_to_bytes(
                recovered_bits
            )

            xor_recovery_time = (
                time.perf_counter() - xor_recovery_start
            )

            # AES Decryption
            aes_decrypt_start = time.perf_counter()

            plaintext = aes.decrypt(
                iv,
                restored_ciphertext
            )

            aes_decrypt_time = (
                time.perf_counter() - aes_decrypt_start
            )

            receiver_total_time = (
                extraction_time
                + xor_recovery_time
                + aes_decrypt_time
            )

            assert plaintext == message

            # ==================================================
            # Metrics
            # ==================================================

            psnr = metrics.psnr(original, stego)
            mse = metrics.mse(original, stego)
            npcr = metrics.npcr(original, stego)
            entropy = metrics.entropy(stego)
            ssim = metrics.ssim(original, stego)
            q_index = metrics.q_index(original, stego)

            # ==================================================
            # Write CSV
            # ==================================================

            writer.writerow([
                image_name,
                resolution,
                text_name,
                payload_size,
                round(aes_encrypt_time, 6),
                round(xor_time, 6),
                round(embedding_time, 6),
                round(sender_total_time, 6),
                round(extraction_time, 6),
                round(xor_recovery_time, 6),
                round(aes_decrypt_time, 6),
                round(receiver_total_time, 6),
                round(psnr, 6),
                round(mse, 10),
                round(npcr, 6),
                round(entropy, 6),
                round(ssim, 8),
                round(q_index, 8)
            ])

            print(
                f"{image_name:20} | "
                f"{text_name:10} | "
                f"Payload: {payload_size:6} B | "
                f"Sender: {sender_total_time:.6f}s | "
                f"Receiver: {receiver_total_time:.6f}s | "
                f"PSNR: {psnr:.2f}"
            )

print("\nFinished.")
print(f"Results saved to {CSV_FILE}")