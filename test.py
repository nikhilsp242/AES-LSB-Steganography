import os
import csv
import time
import cv2

from src.aes import AES256
from src.utility import Utility
from src.dynamicXor import DynamicXOR
from src.embedder import Embedder
from src.metrics import Metrics

from src.sender import Sender
from src.receiver import Receiver


# ============================================================
# Configuration
# ============================================================

IMAGE_DIR = "data/images"
TEXT_DIR = "data/text"
STEGO_DIR = "results/modified_stego"
RESULTS_DIR = "results"

CSV_FILE = os.path.join(
    RESULTS_DIR,
    "results1.csv"
)

SUPPORTED_IMAGE_FORMATS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
    ".tif"
)

# iv = b"1234567890123456"

# ============================================================
# Create directories
# ============================================================

os.makedirs(STEGO_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


# ============================================================
# Initialize components
# ============================================================

key = b"12345678901234567890123456789012"

aes = AES256(key)
utility = Utility()
dxor = DynamicXOR()
embedder = Embedder()
metrics = Metrics()

sender = Sender(
    aes,
    utility,
    dxor,
    embedder
)

receiver = Receiver(
    aes,
    utility,
    dxor,
    embedder
)


# ============================================================
# Get image files
# ============================================================

image_names = sorted(
    name
    for name in os.listdir(IMAGE_DIR)
    if name.lower().endswith(SUPPORTED_IMAGE_FORMATS)
)


# ============================================================
# Get payload files
# ============================================================

payload_names = sorted(
    name
    for name in os.listdir(TEXT_DIR)
    if name.lower().endswith(".txt")
)


# ============================================================
# Display experiment information
# ============================================================

print("=" * 80)
print("EXPERIMENT CONFIGURATION")
print("=" * 80)

print(f"Cover images : {len(image_names)}")
print(f"Payloads     : {len(payload_names)}")
print(
    f"Total runs   : "
    f"{len(image_names) * len(payload_names)}"
)

print("\nPayload files:")

for payload_name in payload_names:
    print(f"  {payload_name}")


# ============================================================
# Create CSV
# ============================================================

with open(
    CSV_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

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
        "Entropy",
        "SSIM",
        "Q-Index"
    ])


    # ========================================================
    # Loop over cover images
    # ========================================================

    for image_name in image_names:

        image_path = os.path.join(
            IMAGE_DIR,
            image_name
        )

        original = cv2.imread(image_path)

        if original is None:

            print(
                f"\nERROR: Could not read "
                f"{image_name}"
            )

            continue


        height, width = original.shape[:2]

        resolution = f"{width}x{height}"


        print("\n")
        print("=" * 80)
        print(f"IMAGE: {image_name}")
        print(f"RESOLUTION: {resolution}")
        print("=" * 80)


        # ====================================================
        # Loop over payloads
        # ====================================================

        for payload_name in payload_names:

            print("\n" + "-" * 80)
            print(f"Payload: {payload_name}")
            print("-" * 80)


            # ------------------------------------------------
            # Read payload
            # ------------------------------------------------

            payload_path = os.path.join(
                TEXT_DIR,
                payload_name
            )

            with open(
                payload_path,
                "r",
                encoding="utf-8"
            ) as f:

                message = f.read()


            payload_size = len(
                message.encode("utf-8")
            )

            print(
                f"Payload size: "
                f"{payload_size} bytes"
            )


            # =================================================
            # SENDER
            # =================================================

            sender_start = time.perf_counter()


            # -------------------------------------------------
            # AES Encryption
            # -------------------------------------------------

            aes_start = time.perf_counter()

            iv, ciphertext = aes.encrypt(
                message
            )

            # ciphertext = aes.encrypt_with_iv(message, iv)

            aes_encrypt_time = (
                time.perf_counter()
                - aes_start
            )


            # -------------------------------------------------
            # Convert ciphertext to binary
            # -------------------------------------------------

            binary_ciphertext = (
                utility.bytes_to_binary(
                    ciphertext
                )
            )


            # -------------------------------------------------
            # Dynamic XOR
            # -------------------------------------------------

            xor_start = time.perf_counter()

            dynamic_key = (
                utility.generate_dynamic_key(
                    binary_ciphertext
                )
            )

            embedded_bits = (
                dxor.xor_message(
                    binary_ciphertext,
                    dynamic_key
                )
            )

            xor_time = (
                time.perf_counter()
                - xor_start
            )


            # -------------------------------------------------
            # Embedding
            # -------------------------------------------------

            embed_start = time.perf_counter()

            stego = sender.embedder.embed(
                original.copy(),
                embedded_bits
            )

            embedding_time = (
                time.perf_counter()
                - embed_start
            )


            # -------------------------------------------------
            # Sender total time
            # -------------------------------------------------

            sender_total_time = (
                time.perf_counter()
                - sender_start
            )


            # -------------------------------------------------
            # Save stego image
            # -------------------------------------------------

            image_base = os.path.splitext(
                image_name
            )[0]

            payload_base = os.path.splitext(
                payload_name
            )[0]

            stego_name = (
                f"{image_base}_"
                f"{payload_base}.png"
            )

            stego_path = os.path.join(
                STEGO_DIR,
                stego_name
            )

            success = cv2.imwrite(
                stego_path,
                stego
            )

            if not success:

                print(
                    f"ERROR: Could not save "
                    f"{stego_name}"
                )

                continue


            # =================================================
            # RECEIVER
            # =================================================

            receiver_start = time.perf_counter()


            # -------------------------------------------------
            # Extraction
            # -------------------------------------------------

            extract_start = time.perf_counter()

            extracted_bits = (
                receiver.embedder.extract(
                    stego,
                    len(embedded_bits)
                )
            )

            extraction_time = (
                time.perf_counter()
                - extract_start
            )


            # -------------------------------------------------
            # XOR Recovery
            # -------------------------------------------------

            xor_recovery_start = (
                time.perf_counter()
            )

            recovered_bits = (
                receiver.dxor.recover_message(
                    extracted_bits,
                    dynamic_key
                )
            )

            restored_ciphertext = (
                receiver.utility.binary_to_bytes(
                    recovered_bits
                )
            )

            xor_recovery_time = (
                time.perf_counter()
                - xor_recovery_start
            )


            # -------------------------------------------------
            # AES Decryption
            # -------------------------------------------------

            aes_decrypt_start = (
                time.perf_counter()
            )

            plaintext = (
                receiver.aes.decrypt(
                    iv,
                    restored_ciphertext
                )
            )

            aes_decrypt_time = (
                time.perf_counter()
                - aes_decrypt_start
            )


            # -------------------------------------------------
            # Receiver total time
            # -------------------------------------------------

            receiver_total_time = (
                time.perf_counter()
                - receiver_start
            )


            # -------------------------------------------------
            # Verify message recovery
            # -------------------------------------------------

            assert plaintext == message

            print("Recovery: SUCCESS")


            # =================================================
            # METRICS
            # =================================================

            psnr = metrics.psnr(
                original,
                stego
            )

            mse = metrics.mse(
                original,
                stego
            )

            entropy = metrics.entropy(
                stego
            )

            ssim = metrics.ssim(
                original,
                stego
            )

            q_index = metrics.q_index(
                original,
                stego
            )


            # =================================================
            # Write result to CSV
            # =================================================

            writer.writerow([
                image_name,
                resolution,
                payload_name,
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
                round(entropy, 6),
                round(ssim, 8),
                round(q_index, 8)
            ])


            # =================================================
            # Display result
            # =================================================

            print(
                f"Sender time   : "
                f"{sender_total_time:.6f}s"
            )

            print(
                f"Receiver time : "
                f"{receiver_total_time:.6f}s"
            )

            print(
                f"PSNR          : "
                f"{psnr:.6f}"
            )

            print(
                f"MSE           : "
                f"{mse:.10f}"
            )

            print(
                f"Entropy       : "
                f"{entropy:.6f}"
            )

            print(
                f"SSIM          : "
                f"{ssim:.8f}"
            )

            print(
                f"Q-Index       : "
                f"{q_index:.8f}"
            )


# ============================================================
# Finished
# ============================================================

print("\n")
print("=" * 80)
print("ALL EXPERIMENTS COMPLETED")
print("=" * 80)

print(
    f"Images processed : {len(image_names)}"
)

print(
    f"Payloads tested  : {len(payload_names)}"
)

print(
    f"Total experiments: "
    f"{len(image_names) * len(payload_names)}"
)

print(
    f"\nResults saved to:\n{CSV_FILE}"
)