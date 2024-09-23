import nltk
import numpy as np
import random


"""Call finish_sentence on n-1 parts of the given sentence.
    Go to get_probabilities, create your n_grams dictionary from your corpus, check if context appears
    If context appears, find the maximum probability word
    If the context doesn't appear, 
"""


def finish_sentence(sentence, n: int, corpus, randomize=False):
    """Adds word to your sentence until reaches 10 tokens or reaches ! ? or ."""
    while (
        len(sentence) < 10
        and "!" not in sentence
        and "?" not in sentence
        and "." not in sentence
    ):
        all_grams = list_of_ngrams(corpus, n)
        next_word = get_probabilities(sentence, n, corpus, all_grams, randomize)
        sentence.append(next_word)
    return sentence


def get_probabilities(sentence, n, corpus, all_grams, randomize):
    """Get probabilities for each word in your vocabulary, stupid backoff if it isn't in your context dictionary"""
    most_likely_word = None
    max_prob = 0
    if (
        len(sentence) < n - 1
    ):  # if your input sentence is less than the n, put in fillers so it'll trigger stupid backoff
        while len(sentence) <= n - 1:
            sentence.insert(0, " ")
    context = tuple(sentence[-(n - 1) :])
    for i in range(len(sentence) - 1):
        if sentence[i] == " ":
            sentence.pop(i)
    vocab = make_vocabulary(corpus)

    if randomize is True:
        return pick_random(context, n, all_grams, vocab)
    else:
        for word in vocab:
            prob = get_score(word, context, n, all_grams)
            vocab[word] = prob
            if prob > max_prob:
                max_prob = prob
                most_likely_word = word
            elif prob == max_prob:
                if word < most_likely_word:
                    most_likely_word = word
    return (
        most_likely_word
        # sorted(vocab.items(), key=lambda x: (-x[1], x[0]), reverse=False)[:20], - checks vocab probabilities sorted
    )


def get_score(word, context, n, all_grams, alpha=0.4):
    n_grams = all_grams[n]
    if context in n_grams.keys() and word in n_grams[context].keys():
        prob = n_grams[context][word] / sum(n_grams[context].values())
        return prob
    else:
        return alpha * get_score(word, context[1:], n - 1, all_grams)


def pick_random(context, n, all_grams, vocab):
    for word in vocab:
        prob = get_score(word, context, n, all_grams)
        vocab[word] = prob
    return "".join(random.choices(list(vocab.keys()), list(vocab.values())))


def get_ngrams(corpus, n):
    """Create a dictionary of possible n-grams with their next word as a nested dictionary"""
    dict_of_ns = {}
    count = 0
    for i in range(0, len(corpus) - n + 1):
        count += 1
        if tuple(corpus[i : i + n - 1]) in dict_of_ns:
            if corpus[i + n - 1] in dict_of_ns[tuple(corpus[i : i + n - 1])]:
                dict_of_ns[tuple(corpus[i : i + n - 1])][corpus[i + n - 1]] += 1
            else:
                dict_of_ns[tuple(corpus[i : i + n - 1])][corpus[i + n - 1]] = 1
        else:
            dict_of_ns[tuple(corpus[i : i + n - 1])] = {corpus[i + n - 1]: 1}
    return dict_of_ns


def list_of_ngrams(corpus, n):
    all_grams = {}
    while n > 0:
        all_grams[n] = get_ngrams(corpus, n)
        n -= 1
    return all_grams


def make_vocabulary(corpus):
    vocab_dict = {}
    for word in corpus:
        vocab_dict[word] = 0
    return vocab_dict


import csv
import nltk


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


if __name__ == "__main__":
    test_generator()
