from BWT import *
from Entropy import *
from LZ import *
filenames = ["test/enwik7.txt"]
n = 6
def plotBWTMTF():
    matrix = [list(range(50, 15050, 1000))]
    print(matrix[-1])
    for filename in filenames:
        matrix.append([])
        for CHUNK_SIZE in range (50, 15050, 1000):
            f = open(filename, "rb")
            data = f.read()
            enc_data = b''
            for j in range(0, (len(data) - 1) // CHUNK_SIZE + 1):
                enc_data += bwt_encode_sa(data[j * CHUNK_SIZE: min(j * CHUNK_SIZE + CHUNK_SIZE, len(data))])
            enc_data = mtf_encode(enc_data)
            matrix[-1].append(entropy(enc_data, 1))
        print(matrix[-1])

def plotLZSS():
    matrix = [list(range(50, 12000, 1000))]
    print(matrix[-1])
    for filename in filenames:
        matrix.append([])
        for windows_size in range(50, 12000, 1000):
            f = open(filename, "rb")
            data = f.read()
            enc_data = lzss_encode(data, windows_size)
            matrix[-1].append(len(data) / len(enc_data))
            print(f"\t({len(data) / len(enc_data)})")
        print(matrix[-1])

def plotLZW():
    matrix = [[2**x for x in range(9, 21)]]
    print(matrix[-1])
    for filename in filenames:
        matrix.append([])
        for windows_size in [2**x for x in range(9, 21)]:
            f = open(filename, "rb")
            data = f.read()
            enc_data = lzw_encode(data, windows_size)
            matrix[-1].append(len(data) / len(enc_data))
            print(f"\t({len(data) / len(enc_data)})")
        print(matrix[-1])