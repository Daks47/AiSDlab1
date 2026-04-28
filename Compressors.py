from LZ import *
from HuffMan import *
from BWT import *
from Entropy import *
from RLE import *
CHUNK_SIZE = 1024
filenames = ["test/enwik7.txt", "test/exe.exe", "test/Lenna.raw", "test/LennaBW.raw", "test/LennaGS.raw", "test/russian.txt"]
def compressorHA ():
    matrix = []
    for filename in filenames:
        matrix.append([0, 0, 0, False])
        f = open(filename, "rb")
        data = f.read()
        matrix[-1][0] = len(data)
        enc_data = huffman_encode(data)
        matrix[-1][1] = len(enc_data)
        dec_data = huffman_decode(enc_data)
        matrix[-1][2] = len(dec_data)
        matrix[-1][3] = dec_data == data
    print(matrix)

def compressorRLE ():
    matrix = []
    for filename in filenames:
        matrix.append([0, 0, 0, False])
        f = open(filename, "rb")
        data = f.read()
        matrix[-1][0] = len(data)
        enc_data = rle_encode(data)
        matrix[-1][1] = len(enc_data)
        dec_data = rle_decode(enc_data)
        matrix[-1][2] = len(dec_data)
        matrix[-1][3] = dec_data == data
    print(matrix)

def compressorBWTRLE ():
    matrix = []
    for filename in filenames:
        matrix.append([0, 0, 0, False])
        f = open(filename, "rb")
        data = f.read()
        matrix[-1][0] = len(data)
        enc_data = b''
        for j in range(0, len(data) // CHUNK_SIZE + 1):
            enc_data += bwt_encode_sa(data[j * CHUNK_SIZE: min(j * CHUNK_SIZE + CHUNK_SIZE, len(data))])
        enc_data = rle_encode(enc_data)
        matrix[-1][1] = len(enc_data)
        dec_data = rle_decode(enc_data)
        dec_data_full = b''
        for j in range(0, len(dec_data) // (CHUNK_SIZE + 3) + 1):
            dec_data_full += bwt_decode_full(
                dec_data[j * (CHUNK_SIZE + 3): min(j * (CHUNK_SIZE + 3) + CHUNK_SIZE + 3, len(dec_data))])
        matrix[-1][2] = len(dec_data_full)
        matrix[-1][3] = dec_data_full == data
    print(matrix)

def compressorBWTMTFHA ():
    matrix = []
    for filename in filenames:
        matrix.append([0, 0, 0, False])
        f = open(filename, "rb")
        data = f.read()
        matrix[-1][0] = len(data)
        enc_data = b''
        for j in range(0, len(data) // CHUNK_SIZE + 1):
            enc_data += bwt_encode_sa(data[j * CHUNK_SIZE: min(j * CHUNK_SIZE + CHUNK_SIZE, len(data))])
        enc_data = huffman_encode(mtf_encode(enc_data))
        matrix[-1][1] = len(enc_data)
        dec_data = mtf_decode(huffman_decode(enc_data))
        dec_data_full = b''
        for j in range(0, len(dec_data) // (CHUNK_SIZE + 3) + 1):
            dec_data_full += bwt_decode_full(
                dec_data[j * (CHUNK_SIZE + 3): min(j * (CHUNK_SIZE + 3) + CHUNK_SIZE + 3, len(dec_data))])
        matrix[-1][2] = len(dec_data_full)
        matrix[-1][3] = dec_data_full == data
    print(matrix)

def compressorBWTMTFRLEHA ():
    matrix = []
    for filename in filenames:
        matrix.append([0, 0, 0, False])
        f = open(filename, "rb")
        data = f.read()
        matrix[-1][0] = len(data)
        enc_data = b''
        for j in range(0, len(data) // CHUNK_SIZE + 1):
            enc_data += bwt_encode_sa(data[j * CHUNK_SIZE: min(j * CHUNK_SIZE + CHUNK_SIZE, len(data))])
        enc_data = huffman_encode(rle_encode(mtf_encode(enc_data)))
        matrix[-1][1] = len(enc_data)
        dec_data = mtf_decode(rle_decode(huffman_decode(enc_data)))
        dec_data_full = b''
        for j in range(0, len(dec_data) // (CHUNK_SIZE + 3) + 1):
            dec_data_full += bwt_decode_full(
                dec_data[j * (CHUNK_SIZE + 3): min(j * (CHUNK_SIZE + 3) + CHUNK_SIZE + 3, len(dec_data))])
        matrix[-1][2] = len(dec_data_full)
        matrix[-1][3] = dec_data_full == data
    print(matrix)

def compressorLZSS ():
    matrix = []
    for filename in filenames:
        matrix.append([0, 0, 0, False])
        f = open(filename, "rb")
        data = f.read()
        matrix[-1][0] = len(data)
        enc_data = lzss_encode(data)
        matrix[-1][1] = len(enc_data)
        dec_data = lzss_decode(enc_data)
        matrix[-1][2] = len(dec_data)
        matrix[-1][3] = dec_data == data
    print(matrix)

def compressorLZSSHA ():
    matrix = []
    for filename in filenames:
        matrix.append([0, 0, 0, False])
        f = open(filename, "rb")
        data = f.read()
        matrix[-1][0] = len(data)
        enc_data = huffman_encode(lzss_encode(data))
        matrix[-1][1] = len(enc_data)
        dec_data = lzss_decode(huffman_decode(enc_data))
        matrix[-1][2] = len(dec_data)
        matrix[-1][3] = dec_data == data
    print(matrix)

def compressorLZW ():
    matrix = []
    for filename in filenames:
        matrix.append([0, 0, 0, False])
        f = open(filename, "rb")
        data = f.read()
        matrix[-1][0] = len(data)
        enc_data = lzw_encode(data)
        matrix[-1][1] = len(enc_data)
        dec_data = lzw_decode(enc_data)
        matrix[-1][2] = len(dec_data)
        matrix[-1][3] = dec_data == data
    print(matrix)

def compressorLZWHA ():
    matrix = []
    for filename in filenames:
        matrix.append([0, 0, 0, False])
        f = open(filename, "rb")
        data = f.read()
        matrix[-1][0] = len(data)
        enc_data = huffman_encode(lzw_encode(data))
        matrix[-1][1] = len(enc_data)
        dec_data = lzw_decode(huffman_decode(enc_data))
        matrix[-1][2] = len(dec_data)
        matrix[-1][3] = dec_data == data
    print(matrix)