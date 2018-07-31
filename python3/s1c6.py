# This is free and unencumbered software released into the public domain

import sys
import numpy as np
from base64 import b64decode
from s1c5 import repeating_xor
from collections import Counter
import random

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
    counts = Counter(input_bin.upper()).items()
    chars = np.array([chr(c) for c, _ in counts])
    freqs = np.array([v for _, v in counts])/len(input_bin)
    expected_freqs = [
        ("A",8.167),
        ("B",1.492),
        ("C",2.782),
        ("D",4.253),
        ("E",12.702),
        ("F",2.228),
        ("G",2.015),
        ("H",6.094),
        ("I",6.966),
        ("J",0.153),
        ("K",0.772),
        ("L",4.025),
        ("M",2.406),
        ("N",6.749),
        ("O",7.507),
        ("P",1.929),
        ("Q",0.095),
        ("R",5.987),
        ("S",6.327),
        ("T",9.056),
        ("U",2.758),
        ("V",0.978),
        ("W",2.360),
        ("X",0.150), 
        ("Y",1.974),
        ("Z",0.074)
    ]

    score = 1

    for letter, exp_freq in expected_freqs:
        if letter in chars:
            score += abs((exp_freq/100) - freqs[list(chars).index(letter)])
        elif letter == " ":
            score += 0
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