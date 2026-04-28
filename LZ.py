from math import log2, floor
from bitstring import BitArray

def lz77_encode(data: bytes, window_size=255) -> bytes:
    i = 0
    n = len(data)
    out = bytearray()

    while i < n:
        best_offset = 0
        best_length = 0

        start = max(0, i - window_size)

        for j in range(start, i):
            length = 0
            while (i + length < n and
                   data[j + length] == data[i + length] and
                   length < 255):
                length += 1

            if length > best_length:
                best_length = length
                best_offset = i - j

        next_byte = data[i + best_length] if i + best_length < n else 0

        out.extend(best_offset.to_bytes(2, 'big'))
        out.append(best_length)
        out.append(next_byte)

        i += best_length + 1

    return bytes(out)

def lz77_decode(data: bytes) -> bytes:
    i = 0
    out = bytearray()

    while i < len(data):
        offset = int.from_bytes(data[i:i+2], 'big')
        length = data[i+2]
        symbol = data[i+3]
        i += 4

        if offset == 0:
            out.append(symbol)
        else:
            start = len(out) - offset
            for j in range(length):
                out.append(out[start + j])
            out.append(symbol)

    return bytes(out)


def lzss_encode(data: bytes, window_size=255) -> bytes:
    i = 0
    out = BitArray()
    bytes_to_write = floor(1/8 * log2(window_size)) + 1

    while i < len(data):
        best_offset = 0
        best_length = 0

        start = max(0, i - window_size)

        for j in range(start, i):
            length = 0
            while (i + length < len(data) and
                   data[j + length] == data[i + length] and
                   length < 255):
                length += 1

            if length > best_length:
                best_length = length
                best_offset = i - j

        if best_length != 0:
            out += BitArray([1])
            out += BitArray(bytes=best_offset.to_bytes(bytes_to_write, byteorder='big'))
            out += BitArray(bytes=best_length.to_bytes(bytes_to_write, byteorder='big'))
            i += best_length
        else:
            out += BitArray([0])
            out += BitArray(bytes=data[i:i+1])
            i += 1

    extra_zeros = ((8 - len(out) % 8) % 8).to_bytes(1, "big")
    return extra_zeros + bytes_to_write.to_bytes(1, "big") + out.tobytes()


def lzss_decode(data: bytes) -> bytes:
    i = 0
    extra_zeros = int.from_bytes(data[:1], "big")
    bytes_to_read = int.from_bytes(data[1:2], "big")
    out = bytearray()
    bits = BitArray(bytes=data[2:])

    if extra_zeros != 0:
        bits = bits[:-extra_zeros]

    while i < len(bits):
        if bits[i]:
            offset = int.from_bytes(bits[i + 1:i+1 + bytes_to_read * 8].tobytes(), byteorder="big")
            length = int.from_bytes(bits[i+1 + bytes_to_read * 8:i+1 + bytes_to_read * 16].tobytes(), byteorder="big")
            i += 1 + 16 * bytes_to_read

            start = len(out) - offset
            for j in range(length):
                out.append(out[start + j])
        else:
            out.extend(bits[i + 1: i + 9].tobytes())
            i += 9
    return bytes(out)

def lz78_encode(data: bytes) -> bytes:
    dictionary = {b"": 0}
    current = b""
    out = bytearray()

    for byte in data:
        new = current + bytes([byte])

        if new in dictionary:
            current = new
        else:
            out.extend(dictionary[current].to_bytes(2, 'big'))
            out.append(byte)
            dictionary[new] = len(dictionary)
            current = b""

    if current:
        out.extend(dictionary[current].to_bytes(2, 'big'))
        out.append(0)

    return bytes(out)

def lz78_decode(data: bytes) -> bytes:
    dictionary = {0: b""}
    out = bytearray()

    i = 0
    while i < len(data):
        idx = int.from_bytes(data[i:i+2], 'big')
        symbol = data[i+2]
        i += 3

        entry = dictionary[idx] + (bytes([symbol]) if symbol != 0 else b"")
        out.extend(entry)

        dictionary[len(dictionary)] = entry

    return bytes(out)

def lzw_encode(data: bytes, max_dict=4096) -> bytes:
    dictionary = {bytes([i]): i for i in range(256)}
    current = b""
    out = bytearray()
    bytes_to_write = 4

    for byte in data:
        new = current + bytes([byte])

        if new in dictionary:
            current = new
        else:
            out.extend(dictionary[current].to_bytes(bytes_to_write, 'big'))
            if len(dictionary) < max_dict:
                dictionary[new] = len(dictionary)
            current = bytes([byte])

    if current:
        out.extend(dictionary[current].to_bytes(bytes_to_write, 'big'))

    return max_dict.to_bytes(4, "big") + bytes(out)

def lzw_decode(f_data: bytes) -> bytes:
    dictionary = {i: bytes([i]) for i in range(256)}
    max_dict = int.from_bytes(f_data[:4], "big")
    bytes_to_read = 4
    data = f_data[4:]
    i = 0
    codes = []

    while i < len(data):
        codes.append(int.from_bytes(data[i:i+bytes_to_read], 'big'))
        i += bytes_to_read

    prev = dictionary[codes[0]]
    out = bytearray(prev)

    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        else:
            entry = prev + prev[:1]

        out.extend(entry)

        if len(dictionary) < max_dict:
            dictionary[len(dictionary)] = prev + entry[:1]

        prev = entry

    return bytes(out)