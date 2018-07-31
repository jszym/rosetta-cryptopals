# This is free and unencumbered software released into the public domain

from s1c3 import is_english
import numpy as np

if __name__ == "__main__":

    with open("../data/s1c4.txt", "r") as f:

        best_scores = []
        best_outputs = []

        for line in f.readlines():
            input_bin = bytes.fromhex(line.strip())
            outputs = []
            scores = []
            for key in range(0,256):
                output = bytes([b ^ key for b in input_bin])
                score = is_english(output)

                outputs.append(output)
                scores.append(score)

            candidate_idx = np.argsort(np.array(scores))[-1]
            best_scores.append(scores[candidate_idx])
            best_outputs.append(outputs[candidate_idx])

        overall_best_idx = np.argsort(np.array(best_scores))[-1]

        print(best_scores[overall_best_idx], best_outputs[overall_best_idx].decode("utf8"))