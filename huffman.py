import heapq
import bittools

class Node:
    def __init__(self, symbol=None, frequency=None, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency

def huffman_enc(cbytes):
    huff_bytes = bytearray() # initialize output bytearray
    freq = freq_eval(cbytes, True) # make byte frequency table
    root = build_huffman_tree(freq) # build huffman tree from frequency table
    huffman_codes = generate_huffman_codes(root) # generate codes from huffman tree
    nodes = serialize(root) # serializes the huffman tree's root
    hufftree = serial_to_squeeze_tree(nodes, len(huffman_codes)) # serializes the rest of the tree
    huff_bytes.extend(hufftree) # adds huffman tree to output
    cdat = huffman_encode(cbytes, huffman_codes) # encodes the data with the tree
    huff_bytes.extend(cdat) # adds huffman coded data to output

    return huff_bytes

def huffman_dec(cbytes):
    huffsize = cbytes[0]+cbytes[1]*256 # get tree size
    seek=2 # seek at tree start
    hufftree = cbytes[seek:seek+(huffsize*4)] # extract tree
    seek+=(huffsize*4) # seek at codepoints start
    huffman_points = huffman_decode(hufftree) # get huffman code points
    dec_bytes = dehuffman(cbytes[seek:], huffman_points) # decode the data with the tree

    return dec_bytes

def serialize(node: huffman.Node, nodes=None):
    parent = False
    if nodes is None:
        parent = True
        nodes = []

    if node.left is None and node.right is None:
        return -(node.symbol + 1)

    index = len(nodes) // 2
    nodes.append(None)
    nodes.append(None)

    left = serialize(node.left, nodes)
    right = serialize(node.right, nodes)
    nodes[index*2] = left
    nodes[index*2+1] = right

    if parent:
        return nodes
    else:
        return index

def serial_to_squeeze_tree(serial: list, nc: int):
    hufftree = bytearray(int(nc-1).to_bytes(2, "little"))
    for val in serial:
        hufftree.extend(val.to_bytes(2, "little", signed=True))
    return hufftree

def huffman_encode(data: bytes, huffman_tree: dict):
    huffbuffer = []
    cdat = bytearray()

    for b in data: # itterate over data and get huffman codes
        huffbuffer.extend(huffman_tree[b])
        while len(huffbuffer) >= 8: # dump huffman codes into octet stream
            cdat.append(bittools.boollist_to_int_var(huffbuffer[0:8][::-1])) # The Format Packs Huffman LSB, not MSB
            huffbuffer = huffbuffer[8:]

    huffbuffer.extend(huffman_tree[256]) # add EOF marker

    while len(huffbuffer) >= 8: # dump huffman codes into octet stream
        cdat.append(bittools.boollist_to_int_var(huffbuffer[0:8][::-1])) # The Format Packs Huffman LSB, not MSB. You needed to see this twice xD
        huffbuffer = huffbuffer[8:]

    if huffbuffer: # flush anything remaining
        while len(huffbuffer) < 8:
            huffbuffer.append(False) # pad
        cdat.append(bittools.boollist_to_int_var(huffbuffer[::-1]))

    return cdat

def huffman_decode(tree: bytes):
    serial = []
    for p in range(0, len(tree), 2):
        serial.append(int.from_bytes(tree[p:p+2], "little", signed=True)) # unpack huffman tree from bitstream

    #print(serial) - debug: print out serialized tree
    return serial

def dehuffman(huffdat: bytes, huffman_points: list):
    buffer_floor = 64 # keep at least 64 bits of data loaded into the buffer. This gives the decoder a max code length of 64. smaller size = faster, but less compatible with SQ files.
    decode_buffer = []
    seek = 0 # start at index 0
    output = bytearray()

    while True: # continue forever until a break is called

        while len(decode_buffer) < buffer_floor and seek < len(huffdat): # refill buffer if its possible
            decode_buffer.extend(bittools.byte_to_boollist(huffdat[seek])[::-1])
            seek+=1

        codelen = 0 # length of code, index position in decode_buffer
        pointed_index = 0 # points to the location in huffman points

        while True:
            if huffman_points[(pointed_index*2)+int(decode_buffer[codelen])] < 0:
                val = -(huffman_points[(pointed_index*2)+int(decode_buffer[codelen])]+1)
                if val == 256: # EOF
                    return output # exit function
                output.append(val)
                decode_buffer = decode_buffer[codelen+1:] # consume bytes
                break
            else:
                pointed_index = huffman_points[(pointed_index*2)+int(decode_buffer[codelen])]
            codelen+=1

def freq_eval(dat: bytes, eof: bool = False):
    # generate frequency table for huffman coding
    freqtable = []
    for _ in range(256):
        freqtable.append(0)

    if eof:
        freqtable.append(1) # this adds a node with value 256, which marks the end of the squeeze file

    for b in dat:
        freqtable[b]+=1
    return freqtable

def build_huffman_tree(freq_table):
    # Create a priority queue of nodes
    priority_queue = []
    for b, o in enumerate(freq_table):
        if o: # filter entries with zero occurences
            priority_queue.append(Node(b, o))

    heapq.heapify(priority_queue)

    # Build the Huffman tree
    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(frequency=left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

def generate_huffman_codes(node, code=[], huffman_codes=None):
    # recursively generate the huffman table
    if huffman_codes is None:
        huffman_codes = {}

    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code

        generate_huffman_codes(node.left, code+[False], huffman_codes)
        generate_huffman_codes(node.right, code+[True], huffman_codes)

    return huffman_codes

# Given example
#chars = ['a', 'b', 'c', 'd', 'e', 'f']
#freq = [4, 7, 15, 17, 22, 42]

# Build the Huffman tree
#root = build_huffman_tree(chars, freq)

# Generate Huffman codes
#huffman_codes = generate_huffman_codes(root)

# Print Huffman codes
#for char, code in huffman_codes.items():
#    print(f"Character: {char}, Code: {code}")

# code taken from https://www.geeksforgeeks.org/dsa/huffman-coding-in-python/
# Modified to use a frequency table instead
