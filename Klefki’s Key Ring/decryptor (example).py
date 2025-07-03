# decrypt.py
import pathlib
import tinysha                 # uses the KEY inside

# 1. read the ciphertext
cipher = pathlib.Path("mysterious.png").read_bytes()

# 2. reproduce the exact keystream that was used
ks = tinysha.keystream(len(cipher))

# 3. XOR → plaintext
plain = bytes(c ^ k for c, k in zip(cipher, ks))

# 4. split it: everything except the last 64 bytes is the image,
#    the final 64 bytes contain the flag padded with NULs (0x00)
img_data   = plain[:-64]
flag_chunk = plain[-64:]

# 5. save the recovered PNG so you can open it
pathlib.Path("solved.png").write_bytes(img_data)

# 6. print the flag (strip the padding NULs first)
print("FLAG =>", flag_chunk.rstrip(b"\0").decode("utf-8", errors="ignore"))
