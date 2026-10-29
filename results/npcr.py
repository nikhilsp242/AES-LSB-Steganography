import os
import csv
import cv2
import numpy as np


# ============================================================
# Configuration
# ============================================================

STEGO_A_DIR = "stego_A"
STEGO_B_DIR = "stego_B"

RESULTS_DIR = "results"
CSV_FILE = os.path.join(
    RESULTS_DIR,
    "npcr_results.csv"
)


# ============================================================
# Create results directory
# ============================================================

os.makedirs(RESULTS_DIR, exist_ok=True)


# ============================================================
# NPCR Function
# ============================================================

def npcr(image_a, image_b):

    if image_a.shape != image_b.shape:
        raise ValueError(
            "Images must have the same dimensions"
        )

    # A pixel is considered changed if ANY
    # of its RGB channels differs.
    changed_pixels = np.sum(
        np.any(image_a != image_b, axis=2)
    )

    total_pixels = (
        image_a.shape[0] *
        image_a.shape[1]
    )

    return (
        changed_pixels /
        total_pixels
    ) * 100


# ============================================================
# Get files
# ============================================================

files_a = sorted(
    name
    for name in os.listdir(STEGO_A_DIR)
    if name.lower().endswith(".png")
)

files_b = sorted(
    name
    for name in os.listdir(STEGO_B_DIR)
    if name.lower().endswith(".png")
)


# ============================================================
# Check file sets
# ============================================================

if set(files_a) != set(files_b):

    missing_from_b = set(files_a) - set(files_b)
    missing_from_a = set(files_b) - set(files_a)

    if missing_from_b:
        print(
            "Missing from stego_B:"
        )

        for name in sorted(missing_from_b):
            print(f"  {name}")

    if missing_from_a:
        print(
            "Missing from stego_A:"
        )

        for name in sorted(missing_from_a):
            print(f"  {name}")

    raise ValueError(
        "The two directories do not contain "
        "the same set of filenames."
    )


# ============================================================
# Run NPCR experiment
# ============================================================

results = []


for filename in files_a:

    path_a = os.path.join(
        STEGO_A_DIR,
        filename
    )

    path_b = os.path.join(
        STEGO_B_DIR,
        filename
    )


    # --------------------------------------------------------
    # Read images
    # --------------------------------------------------------

    image_a = cv2.imread(
        path_a
    )

    image_b = cv2.imread(
        path_b
    )


    if image_a is None:
        print(
            f"Could not read: {path_a}"
        )
        continue

    if image_b is None:
        print(
            f"Could not read: {path_b}"
        )
        continue


    # --------------------------------------------------------
    # Resolution
    # --------------------------------------------------------

    height, width = image_a.shape[:2]

    resolution = (
        f"{width}x{height}"
    )


    # --------------------------------------------------------
    # Calculate NPCR
    # --------------------------------------------------------

    value = npcr(
        image_a,
        image_b
    )


    # --------------------------------------------------------
    # Extract payload name
    # --------------------------------------------------------

    # Example:
    # baboon_500B.png
    #
    # → 500B

    base_name = os.path.splitext(
        filename
    )[0]

    payload = base_name.split("_")[-1]


    # --------------------------------------------------------
    # Store result
    # --------------------------------------------------------

    results.append([
        filename,
        resolution,
        payload,
        value
    ])


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print(
        f"{filename:25} | "
        f"{resolution:10} | "
        f"NPCR = {value:.6f}%"
    )


# ============================================================
# Save CSV
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
        "NPCR"
    ])

    for row in results:

        writer.writerow([
            row[0],
            row[1],
            row[2],
            round(row[3], 6)
        ])


# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 70)
print("NPCR EXPERIMENT COMPLETED")
print("=" * 70)

print(
    f"Image pairs compared : "
    f"{len(results)}"
)

print(
    f"Results saved to     : "
    f"{CSV_FILE}"
)