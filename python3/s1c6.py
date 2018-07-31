# This is free and unencumbered software released into the public domain

import sys
import numpy as np
from base64 import b64decode
from s1c5 import repeating_xor
from collections import Counter
import pickle

def hamming(x, y):
    """Calculate the Hamming distance between two bit strings"""
    if len(x) != len(y):
        None
    count, z = 0, int.from_bytes(repeating_xor(x, y), byteorder=sys.byteorder)
    while z:
        count += 1
        z &= z - 1  # magic!
    return count

def is_english(input_bin):
    counts = Counter(input_bin).items()
    chars = np.array([chr(c) for c, _ in counts])
    freqs = np.array([v for _, v in counts])/len(input_bin)
    with open("../data/freq_en.pickle", "rb") as f:
        expected_freqs = pickle.load(f)

    score = 1

    for letter, exp_freq in expected_freqs:
        if letter in chars:
            score += abs((exp_freq) - freqs[list(chars).index(letter)])
        else:
            score += 1 

    return score

assert hamming(b"this is a test", b"wokka wokka!!!") == 37

with open("../data/s1c6.txt", "r") as f:
    cipher = b64decode("".join(f.read().split("\n")))

cipher_length = len(cipher)
distances = []

for keysize in range(2,40):
    
    key_distances = []

    for i in range(25):
        a = cipher[keysize*i:keysize*(i+1)]
        b = cipher[keysize*(i+1):keysize*(i+2)]
        key_distances.append(hamming(a,b)/keysize)
    distances.append(np.average(key_distances))

likely_keysizes = np.argsort(distances)[0:3]+2

for likely_keysize in likely_keysizes:
    
    blocks = [[] for i in range(likely_keysize)]

    for i, b in enumerate(cipher):
        blocks[i%likely_keysize].append(b)

    num_key_candidates = 3

    keys = [[] for i in range(num_key_candidates)]

    for block in blocks:
        block_scores = []
        block_keys = []
        for key in range(256):
            output = bytes([b ^ key for b in block])
            block_scores.append(is_english(output))
            block_keys.append(key)
        
        for i in range(num_key_candidates):
            keys[i].append(np.argsort((block_scores))[i])

    for key in keys:
        print(bytes(key).decode("utf8"))