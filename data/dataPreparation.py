import os
import cv2

INPUT_DIR = "original_images"
OUTPUT_DIR = "images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

sizes = [128, 256, 512, 1024]

for image_name in os.listdir(INPUT_DIR):

    if not image_name.lower().endswith((".tif", ".tiff", ".png", ".jpg", ".jpeg")):
        continue

    path = os.path.join(INPUT_DIR, image_name)

    image = cv2.imread(path)

    if image is None:
        continue

    filename = os.path.splitext(image_name)[0]

    for size in sizes:

        resized = cv2.resize(
            image,
            (size, size),
            interpolation=cv2.INTER_CUBIC
        )

        output_name = f"{filename}_{size}.png"

        cv2.imwrite(
            os.path.join(OUTPUT_DIR, output_name),
            resized
        )

        print(output_name)

print("\nDataset preparation completed.")