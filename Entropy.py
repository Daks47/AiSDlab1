import math
from collections import Counter

def entropy(data: bytes, Ms=1) -> float:
    # разбиваем на символы длины Ms
    symbols = [data[i:i+Ms] for i in range(0, len(data), Ms)]
    total = len(symbols)

    freq = Counter(symbols)

    H = 0.0
    for count in freq.values():
        p = count / total
        H -= p * math.log2(p)

    return H

def mtf_encode(data: bytes) -> bytes:
    table = list(range(256))
    result = []

    for byte in data:
        index = table.index(byte)
        result.append(index)

        # move to front
        table.pop(index)
        table.insert(0, byte)

    return bytes(result)

def mtf_decode(data: bytes) -> bytes:
    table = list(range(256))
    result = []

    for index in data:
        symbol = table[index]
        result.append(symbol)

        table.pop(index)
        table.insert(0, symbol)

    return bytes(result)

def arithmetic_encode(data, probs):
    low = 0.0
    high = 1.0

    for symbol in data:
        range_ = high - low
        sym_low, sym_high = probs[symbol]

        high = low + range_ * sym_high
        low = low + range_ * sym_low

    return (low + high) / 2