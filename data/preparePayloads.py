import os

MASTER_FILE = "master_message.txt"
OUTPUT_DIR = "text"

os.makedirs(OUTPUT_DIR, exist_ok=True)

payloads = {
    "100B.txt": 100,
    "250B.txt": 250,
    "500B.txt": 500,
    "1KB.txt": 1024,
    "2KB.txt": 2048,
    "4KB.txt": 4096,
    "8KB.txt": 8192,
    "16KB.txt": 16384,
    "32KB.txt": 32768,
    "64KB.txt": 65536
}

with open(MASTER_FILE, "rb") as f:
    master = f.read()

for filename, size in payloads.items():

    payload = master[:size]

    with open(os.path.join(OUTPUT_DIR, filename), "wb") as out:
        out.write(payload)

    print(f"{filename:<10} {len(payload):>8} bytes")

print("\nPayload generation completed.")