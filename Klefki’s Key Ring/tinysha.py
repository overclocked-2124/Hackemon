# tinysha.py
import hashlib, struct

KEY = b"REPLACE_THIS_WITH_THE_SECRET_KEY_YOU_DISCOVERED"         # keep this private
def keystream(n):
    """Return n bytes from the PRNG."""
    out = bytearray()
    counter = 0
    while len(out) < n:
        h = hashlib.sha256(KEY + struct.pack('>I', counter)).digest()
        out.extend(h[:7])            # ***non-standard 56-bit blocks***
        counter += 1
    return bytes(out[:n])
