from pathlib import Path

OUTPUT_FILE = Path("text/master_message.txt")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

paragraphs = [
"""Image steganography is the process of concealing secret information inside a digital image while preserving its visual appearance. Unlike cryptography, which hides the content of a message, steganography hides the existence of the message itself. A successful steganographic system should provide imperceptibility, security, robustness, and sufficient embedding capacity.""",

"""The Advanced Encryption Standard (AES) is a symmetric block cipher widely used to secure confidential information. AES supports key sizes of 128, 192, and 256 bits. It performs multiple rounds of substitution, permutation, and mixing operations to transform plaintext into ciphertext while resisting known cryptographic attacks.""",

"""Least Significant Bit substitution is one of the most popular spatial domain image steganography techniques because of its simplicity and high embedding capacity. Secret bits are embedded by modifying only the least significant bits of pixel values, resulting in minimal perceptual distortion.""",

"""Peak Signal-to-Noise Ratio (PSNR) is commonly used to evaluate image quality after data embedding. Higher PSNR values indicate lower distortion between the original cover image and the generated stego image. In practical image steganography systems, PSNR values above 40 dB generally indicate excellent visual quality.""",

"""Mean Squared Error (MSE) measures the average squared difference between corresponding pixels of the cover image and the stego image. Lower MSE values correspond to smaller embedding distortion and usually lead to higher PSNR values.""",

"""Entropy measures the randomness of an image. A stego image with entropy similar to that of the original image indicates that the embedding process has preserved the statistical characteristics of the cover image, reducing the likelihood of successful steganalysis.""",

"""Network security relies on multiple layers of protection including encryption, authentication, integrity verification, intrusion detection, and access control. Combining cryptographic techniques with information hiding methods provides an additional layer of confidentiality for sensitive communications.""",

"""Digital images are typically represented using three color channels: red, green, and blue. Each channel stores an intensity value ranging from 0 to 255 for every pixel. Modifying only the least significant bit changes the intensity by at most one level, making the alteration nearly imperceptible to the human visual system.""",

"""Python has become one of the most popular programming languages for scientific computing because of its extensive ecosystem of libraries such as NumPy, OpenCV, Pandas, Matplotlib, and SciPy. These libraries simplify image processing, numerical computation, and data visualization tasks.""",

"""Image processing techniques are widely used in medical imaging, satellite remote sensing, autonomous vehicles, industrial inspection, digital forensics, and multimedia communication. Secure image transmission has become increasingly important due to the rapid growth of internet-based applications.""",

"""Machine learning algorithms are capable of identifying complex statistical relationships in high-dimensional data. Although traditional least significant bit steganography does not require machine learning, recent research explores deep learning models for adaptive embedding and steganalysis.""",

"""Cybersecurity aims to protect computer systems, communication networks, and digital assets from unauthorized access, modification, disclosure, disruption, or destruction. Effective security solutions combine prevention, detection, response, and recovery mechanisms.""",

"""Research in image steganography continues to focus on improving embedding capacity, visual quality, robustness against attacks, computational efficiency, and resistance to statistical steganalysis while maintaining secure recovery of the embedded secret message.""",

"""Digital communication systems rely on efficient transmission protocols to ensure reliable delivery of information across wired and wireless networks. Error detection, retransmission strategies, congestion control, and encryption contribute to secure and dependable communication.""",

"""Open-source software has significantly accelerated scientific research by providing freely available implementations of algorithms, datasets, and evaluation tools. Researchers can reproduce experimental results, compare techniques fairly, and propose meaningful improvements over existing methods."""
]

TARGET_SIZE = 1024 * 1024      # 1 MB

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    i = 0

    while f.tell() < TARGET_SIZE:
        f.write(paragraphs[i % len(paragraphs)])
        f.write("\n\n")
        i += 1

print(f"Created {OUTPUT_FILE}")
print(f"Size: {OUTPUT_FILE.stat().st_size:,} bytes")