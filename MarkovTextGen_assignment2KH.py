"""Markov Text Generator.

Patrick Wang, 2024

Resources:
Jelinek 1985 "Markov Source Modeling of Text Generation"
"""

import csv
import nltk

# from mtg import finish_sentence
import csv


# def test_generator():
#     """Test Markov text generator."""
#     corpus = tuple(
#         nltk.word_tokenize(nltk.corpus.gutenberg.raw("austen-sense.txt").lower())
#     )

#     with open("test_examples.csv") as csvfile:
#         csvreader = csv.DictReader(csvfile, delimiter=",")
#         for row in csvreader:
#             words = finish_sentence(
#                 row["input"].split(" "),
#                 int(row["n"]),
#                 corpus,
#                 randomize=False,
#             )
#             print(f"input: {row['input']} (n={row['n']})")
#             print(f"output: {' '.join(words)}")
#             assert words == row["output"].split(" ")


# ------------------------------------------------------------------------------------------
import random
from collections import defaultdict


def finish_sentence(sentence, n, corpus, randomize=False):
    # Initial n-gram (last n-1 tokens from the sentence)
    ngram = tuple(sentence[len(sentence) - n + 1 :])  # correct slicing for n-gram
    sentence_ans = list(sentence)  # Start building the sentence

    # Loop until we meet one of the stopping conditions
    while len(sentence_ans) < 10 and sentence_ans[-1] not in [".", "?", "!"]:

        # Initialize the big dictionary to store ngram and following words counts
        big_dict = defaultdict(lambda: defaultdict(int))

        # Build the dictionary of counts for each following word after the current ngram
        for i in range(len(corpus) - n + 1):
            current_ngram = tuple(
                corpus[i : i + n - 1]
            )  # extract the n-1 length prefix
            next_word = corpus[i + n - 1] if i + n - 1 < len(corpus) else None
            if next_word:
                big_dict[current_ngram][next_word] += 1

        # Get the possible next word counts for the current ngram
        possible_next_words = big_dict.get(ngram, {})

        # Stupid backoff: if no next word found, backoff to a smaller ngram
        if not possible_next_words and len(ngram) > 1:
            ngram = ngram[1:]  # backoff by one token
            continue  # Retry with the shorter ngram

        # If we still don't find a match, stop the sentence
        if not possible_next_words:
            break

        # If randomize is False, pick the most probable word deterministically
        if not randomize:
            # Sort words by frequency, then alphabetically for ties
            next_word = min(
                possible_next_words, key=lambda x: (-possible_next_words[x], x)
            )

        # If randomize is True, pick a word based on its probability
        else:
            total = sum(possible_next_words.values())
            next_word = random.choices(
                list(possible_next_words.keys()), weights=possible_next_words.values()
            )[0]

        # Append the selected next word to the sentence
        sentence_ans.append(next_word)

        # Update the current ngram
        ngram = tuple(sentence_ans[-(n - 1) :])

    return tuple(sentence_ans)


# if __name__ == "__main__":
test_generator()
