# AES-LSB Image Steganography

An educational Python project exploring text hiding in color images. It combines AES encryption with a simple LSB (least significant bit) embedding routine and records image-quality and runtime measurements across sample images and payloads.

This is an experimental implementation inspired by the paper *Dynamic 8-bit XOR algorithm with AES crypto algorithm for image steganography* (Madhu, Vasuhi, and Samydurai, 2024). It is **not a faithful reproduction** of the paper: the paper describes its XOR and AES steps inconsistently, while this code encrypts the text payload and then embeds the resulting ciphertext bits using sequential LSB replacement.

## How it works

For each input text and cover image, [`main.py`](main.py) performs these steps:

1. Encrypts the UTF-8 text with AES-256-CBC and PKCS#7 padding.
2. Converts the ciphertext to bits and XORs it with a repeating `0101...` pattern.
3. Replaces successive image-channel LSBs with those bits.
4. Extracts the bits again in memory, reverses the XOR, decrypts the ciphertext, and checks that the plaintext matches.
5. Calculates runtime and image metrics, then writes a CSV row and a stego image.

The XOR pattern is deterministic and public; it is included to reflect the experiment, not as a security feature. AES provides the encryption in this prototype.

## Requirements

- Python 3.9 or newer
- OpenCV (`opencv-python`)
- NumPy
- `cryptography`

Create and activate a virtual environment, then install the packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install opencv-python numpy cryptography
```

## Run the experiment

From the repository root:

```bash
python main.py
```

The script processes supported images in `data/images/` against `.txt` payloads in `data/text/`. It writes:

- `results/metrics.csv` — timing, PSNR, MSE, NPCR, entropy, correlation-based similarity, and Q-index values.
- `results/stego/` — generated PNG stego images.

Generated stego images and local virtual environments are excluded from Git. The CSV and analysis notebooks currently in `results/` are retained as experiment records; rerunning `main.py` overwrites `results/metrics.csv` and the matching stego images.

The `data/` directory includes sample cover images, prepared text payloads, and scripts used to prepare them. `data/dataPreparation.py` and `data/preparePayloads.py` expect to be run from inside the `data/` directory.

## Metrics and interpretation

The metrics are experimental image comparisons, not proof that hidden data is secure or undetectable. In particular:

- PSNR and MSE describe pixel distortion.
- NPCR counts a pixel as changed if any channel differs; it is not, by itself, evidence of steganographic security.
- Entropy is calculated over all channel values together.
- The method named `ssim` in [`src/metrics.py`](src/metrics.py) computes a per-channel Pearson correlation, **not the standard structural similarity (SSIM) metric**.
- The reported values depend on the selected image, payload, and implementation details. They should not be treated as independently verified reproductions of the paper's results.

## Important limitations

- The AES key in `main.py` is a hard-coded demonstration key. Do not use it to protect real messages.
- AES-CBC does not authenticate ciphertext, so tampering is not reliably detected.
- The IV, payload length, and XOR pattern are not stored in the image. The current script recovers the message during the same run using in-memory values; a saved image alone is not a self-contained message format.
- Embedding uses sequential LSBs and is not robust to image resizing, recompression, or other edits.
- There is no command-line interface for selecting images, payloads, keys, or output paths, and no separate automated test suite at present.

This project is for learning and research discussion, not production security or covert communication.

## Reference

D. Madhu, S. Vasuhi, and A. Samydurai, “Dynamic 8-bit XOR algorithm with AES crypto algorithm for image steganography,” *Signal, Image and Video Processing*, vol. 18, suppl. 1, pp. S429–S445, 2024. [https://doi.org/10.1007/s11760-024-03165-6](https://doi.org/10.1007/s11760-024-03165-6)

The publisher's PDF is not included in this repository. Check the source and licensing terms for any datasets or sample images before redistributing them. No open-source license has been added to this repository yet.
