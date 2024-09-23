"""Markov Text Generator.

Patrick Wang, 2024

Resources:
Jelinek 1985 "Markov Source Modeling of Text Generation"
"""

import csv
import nltk

from mtg import finish_sentence

from collections import defaultdict  # KH


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


# ----------------------------------------------------------------------------------------------------
def finish_sentence(sentence, n, corpus, randomize=False):
    ngram = sentence[len(sentence) - n + 1 :]
    sentence_ans = list(sentence)

    # while length of sentence <= 10 or the last element is not "., ?, !"
    while len(sentence_ans) <= 10 or sentence_ans[-1] not in [".", "?", "!"]:
        # so now we are going to make a dictionary with the ngram variable as the first key, and then create a subdictionary as that keys value
        big_dict = defaultdict(lambda: defaultdict(int))
        # and then for every word in our vocabularly, we need to make it a key in this sub dictionary
        for each_word in corpus:  # INITIAL NGRAM
            big_dict[ngram][
                each_word
            ] = 0  # this just creates a dictionary with 0s for all the words

            for i in range(len(corpus)):
                if corpus[i : n - 2] == ngram and corpus[i + n - 1] == each_word:
                    big_dict[ngram][
                        each_word
                    ] += 1  # add one whereever you see the ngram followed by the word in the corpus

        # STUPID BACKOFF
        for key, value in big_dict[ngram].items():
            if value == 0:
                ngram

    return tuple(sentence_ans)


# if there isnt then we gotta do some shit, aka the key's value is 0 after looking through the whole paragraph
# create a while loop here, while freq =0
#       create a variable called nminusonegram that takes off the first element of the sentence
#       repeat similar process to above, but now just look to see if you can find nminusonegram followed by this word anywhere
#       increase a variable called stupid frequency, when the ngram -1 has an occurrence
#       then update nminusonegram = equal the smaller ngram before continuing
# freq = freq*alpha

# then find the maximum value and get its key
# append that key to sentence
# adjust the ngram variable to shift over


if __name__ == "__main__":
    test_generator()
