from collections import Counter
import numpy as np
import pickle

if __name__ == "__main__":
    with open("../data/corpus_en.txt", "rb") as f:
        corpus = f.read().decode("utf8")
    counts = Counter(corpus).items()

    freqs = [(char, freq/len(corpus)) for char, freq in counts]

    with open("../data/freq_en.pickle", "wb") as f:
        pickle.dump(freqs, f)