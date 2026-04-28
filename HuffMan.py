import heapq
from bitarray import bitarray

class HuffmanTreeNode:
    def __init__(self, frequency, symbol, left_child=None, right_child=None):
        self.frequency = frequency
        self.left = left_child
        self.right = right_child
        self.symbol = symbol

    def __lt__(self, other):
        return self.frequency < other.frequency

def calculate_frequencies(data):
    frequency_map = {}
    for i in range(len(data)):
        frequency_map[data[i:i + 1]] = frequency_map.get(data[i:i + 1], 0) + 1
    return frequency_map

def generate_canonical_codes(code_dict):
    canonical_codes = {}
    code_value = 0
    lengths = range(1, max(code_dict.keys()) + 1)
    metadata_c = (sum([len(x) for x in code_dict.values()]) - 1).to_bytes(1, "big")

    for length in lengths:
        for char in sorted(code_dict.get(length, [])):
            metadata_c += bytes(char)
            canonical_codes[char] = list(map(int, list(bin(code_value)[2:])))
            canonical_codes[char] = ([0] * (length - len(canonical_codes[char])) if len(
                canonical_codes[char]) < length else []) + canonical_codes[char]
            code_value += 1
        code_value <<= 1
    return canonical_codes, metadata_c, lengths

def generate_decoding_canonical_codes(lengths, characters):
    decoding_codes = {}
    code_value = 0
    char_index = 0

    for length in range(len(lengths)):
        for _ in range(lengths[length]):
            code = bin(code_value)[2:]
            code = ('0' * (length + 1 - len(code)) if len(code) < length + 1 else '') + code
            decoding_codes[code] = characters[char_index]
            code_value += 1
            char_index += 1
        code_value <<= 1
    return decoding_codes

def build_huffman_tree(frequencies):
    priority_queue = []

    for symbol, freq in frequencies.items():
        heapq.heappush(priority_queue, HuffmanTreeNode(freq, symbol))

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged_node = HuffmanTreeNode(left.frequency + right.frequency, left.symbol + right.symbol, left, right)
        heapq.heappush(priority_queue, merged_node)

    return heapq.heappop(priority_queue)

def huffman_encode(data):
    frequency_map = calculate_frequencies(data)

    tree_root = build_huffman_tree(frequency_map)
    code_dict = {}
    generate_codes(tree_root, [0] * 32, 0, code_dict)

    encoded_bits = bitarray()

    canonical_codes, metadata_c, length_info = generate_canonical_codes(code_dict)

    metadata_length = length_info[-1].to_bytes(1, "big")
    for length in length_info:
        metadata_length += (len(code_dict.get(length, []))).to_bytes(1, "big")
    for i in range(len(data)):
        encoded_bits += bitarray(canonical_codes[data[i: i + 1]])

    extra_zeros = ((8 - len(encoded_bits) % 8) % 8).to_bytes(1, "big")
    encoded_bits = metadata_length + metadata_c + extra_zeros + encoded_bits.tobytes()

    return encoded_bits

def generate_codes(node, arr, top, code_dict):
    if node.left:
        arr[top] = 0
        generate_codes(node.left, arr, top + 1, code_dict)

    if node.right:
        arr[top] = 1
        generate_codes(node.right, arr, top + 1, code_dict)

    if not node.left and not node.right:
        if len(bitarray(arr[:top])) in code_dict:
            code_dict[len(bitarray(arr[:top]))].append(node.symbol)
        else:
            code_dict[len(bitarray(arr[:top]))] = [node.symbol]


def huffman_decode(encoded_data):
    max_len = int.from_bytes(encoded_data[:1], "big")
    lengths = [int.from_bytes(encoded_data[i + 1:i + 2], "big") for i in range(max_len)]
    num_characters = int.from_bytes(encoded_data[max_len + 1:max_len + 2], "big") + 1
    char_array = [encoded_data[i + max_len + 2:i + max_len + 3] for i in range(num_characters)]
    extra_zeros = int.from_bytes(encoded_data[max_len + num_characters + 2:max_len + num_characters + 3], "big")
    encoded_message = encoded_data[max_len + num_characters + 3:]

    bits = bitarray(endian="big")
    bits.frombytes(encoded_message)

    if extra_zeros != 0:
        bits = bits[:-extra_zeros]

    decoding_codes = generate_decoding_canonical_codes(lengths, char_array)

    buffer = []
    decoded_output = []
    for bit in bits:
        buffer.append(str(int(bit)))
        buffer_str = ''.join(buffer)
        if buffer_str in decoding_codes:
            decoded_output.append(decoding_codes[buffer_str])
            buffer = []
    decoded_output = b''.join(decoded_output)
    return decoded_output