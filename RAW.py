import struct
import os
def save_raw(filename, data, mode):
    h, w = data.shape[:2]
    channels = 1 if len(data.shape) == 2 else 3

    with open(filename, "wb") as f:

        mode_bytes = mode.encode()
        f.write(struct.pack("IIII", w, h, channels, len(mode_bytes)))
        f.write(mode_bytes)

        f.write(data.tobytes())

def compression_ratio(raw_file, compressed_file):
    raw_size = os.path.getsize(raw_file)
    comp_size = os.path.getsize(compressed_file)
    return raw_size / comp_size