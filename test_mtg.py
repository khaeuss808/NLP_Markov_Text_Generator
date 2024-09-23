"""Markov Text Generator.

Patrick Wang, 2024

Resources:
Jelinek 1985 "Markov Source Modeling of Text Generation"
"""

import csv
import nltk

from mtg import finish_sentence


def test_generator():
    """Test Markov text generator."""
    corpus = tuple(
        nltk.word_tokenize(nltk.corpus.gutenberg.raw("austen-sense.txt").lower())
    )

    with open("test_examples.csv") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",")
        for row in csvreader:
            words = finish_sentence(
                row["input"].split(" "),
                int(row["n"]),
                corpus,
                randomize=False,
            )
            print(f"input: {row['input']} (n={row['n']})")
            print(f"output: {' '.join(words)}")
            assert words == row["output"].split(" ")

    # tests that I wrote in addition to Patricks
    sentence = ["she", "was", "not"]
    n = 3
    corpus = nltk.word_tokenize(nltk.corpus.gutenberg.raw("austen-sense.txt").lower())
    randomize = True  # to test random words
    randomized_sentence = finish_sentence(sentence, n, corpus, randomize)
    print(f"Testing randomized sentence: {' '.join(randomized_sentence)}")


if __name__ == "__main__":
    test_generator()
