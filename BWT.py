from collections import defaultdict
def bwt_encode(data: bytes):
    n = len(data)

    # циклические сдвиги
    rotations = [data[i:] + data[:i] for i in range(n)]

    # сортировка
    rotations.sort()

    # последний столбец
    last_column = bytes(row[-1] for row in rotations)

    # индекс исходной строки
    primary_index = rotations.index(data)

    return last_column, primary_index

def bwt_decode(L: bytes, primary_index: int):
    n = len(L)

    # считаем частоты
    count = defaultdict(int)
    for c in L:
        count[c] += 1

    # строим F (первый столбец)
    sorted_chars = sorted(count)
    starts = {}
    total = 0
    for c in sorted_chars:
        starts[c] = total
        total += count[c]

    # LF mapping
    occ = defaultdict(int)
    LF = [0] * n

    for i, c in enumerate(L):
        LF[i] = starts[c] + occ[c]
        occ[c] += 1

    # восстановление
    res = bytearray(n)
    pos = primary_index

    for i in range(n - 1, -1, -1):
        res[i] = L[pos]
        pos = LF[pos]

    return bytes(res)

def bwt_decode_fast(L: bytes, index: int):
    n = len(L)

    # подсчёт символов
    count = defaultdict(int)
    for c in L:
        count[c] += 1

    # стартовые позиции (F)
    sorted_chars = sorted(count)
    starts = {}
    total = 0
    for c in sorted_chars:
        starts[c] = total
        total += count[c]

    # ранги символов
    occ = defaultdict(int)
    LF = []

    for c in L:
        LF.append(starts[c] + occ[c])
        occ[c] += 1

    # восстановление
    res = bytearray(n)
    pos = index

    for i in range(n - 1, -1, -1):
        res[i] = L[pos]
        pos = LF[pos]

    return bytes(res)

def build_cyclic_sa(data: bytes):
    n = len(data)
    return sorted(range(n), key=lambda i: data[i:] + data[:i])

def bwt_from_sa(data: bytes, sa: list[int]):
    n = len(data)
    result = bytearray(n)

    for i in range(n):
        j = sa[i]
        result[i] = data[j - 1] if j != 0 else data[n - 1]

    primary_index = sa.index(0)

    return bytes(result), primary_index

def bwt_encode_sa(data):
    sa = build_cyclic_sa(data)
    encoded = bwt_from_sa(data, sa)
    return encoded[1].to_bytes(3, byteorder='big') + encoded[0]

def bwt_decode_full(data: bytes):
    index = int.from_bytes(data[0:3], byteorder='big')
    encoded = data[3:]
    return bwt_decode_fast(encoded, index)