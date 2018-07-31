# This is free and unencumbered software released into the public domain

from collections import Counter
import numpy as np
import pickle

def is_english(input_bin):
    counts = Counter(input_bin.upper()).items()
    chars = np.array([chr(c) for c, _ in counts])
    freqs = np.array([v for _, v in counts])/len(input_bin)
    with open("../data/freq_en.pickle", "rb") as f:
        expected_freqs = pickle.load(f)
    score1 = 1

    for letter, exp_freq in expected_freqs:
        if letter in chars:
            score1 += abs((exp_freq) - freqs[list(chars).index(letter)])
        elif letter == " ":
            score1 += 0
        else:
            score1 += 1 

    pairs = "TH HE AN RE ER IN ON AT ND ST ES EN OF TE ED OR TI HI AS TO LL EE SS OO TT FF RR NN PP CC".split(" ")

    score2 = 0

    input_len = len(input_bin)
    for i in range(input_len):
        if i+1 < input_len:
            if "".join([chr(input_bin[i]), chr(input_bin[i+1])]).upper() in pairs:
                score2 += 1

    score = score2/score1

    return score

if __name__ == "__main__":

    input_hex = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    input_bin = bytes.fromhex(input_hex)

    scores = []
    outputs = []

    for key in range(0, 256):
        output = bytes([b ^ key for b in input_bin])
        score = is_english(output)
        outputs.append(output)
        scores.append(score)

    best_idx = np.argsort(np.array(scores))[-1]
    print(scores[best_idx], outputs[best_idx].decode("utf8"))