import io, sys, math, re
from collections import defaultdict
import numpy as np


def build_ngram(data, n):
    """
    Parameters:
    data (list of lists): each list is a sentence of the text
    n (int): size of the n-gram

    Returns:
    proba (dictionary of dictionary)
    {
        context: {word:probability of this word given context}
    }


    """
    total_number_words = 0
    counts = defaultdict(lambda: defaultdict(lambda: 0.0))

    for sentence in data:
        sentence = tuple(sentence)
        ## FILL CODE
        # dict can be indexed by tuples
        # store in the same dict all the ngrams
        # by using the context as a key and the word as a value
        for i in range(len(sentence)):
            total_number_words += 1
            for k in range(n):
                if i - k < 0:
                    break
                counts[sentence[i - k : i]][sentence[i]] += 1

    proba = defaultdict(lambda: defaultdict(lambda: 0.0))
    # Build the probabilities from the counts
    # Be careful with how you normalize!

    for context in counts.keys():
        ## FILL CODE
        denom = 0
        for w in counts[context].keys():
            denom += counts[context][w]
        for w in counts[context].keys():
            proba[context][w] = counts[context][w] / denom

    return proba


def get_prob(model, context, w):
    """
    Parameters:
    model (dictionary of dictionary)
    {
        context: {word:probability of this word given context}
    }
    context (list of strings): a sentence
    w(string): the word we need to find it's probability given the context

    Retunrs:
    prob(float): probability of this word given the context
    """

    # code a recursive function over
    # smaller and smaller context
    # to compute the backoff model

    ## FILL CODE

    if context in model and w in model[context]:
        return model[context][w]
    else:
        return 0.4 * get_prob(model, context[1:], w)


def perplexity(model, data, n):
    """
    Parameters:
    model (dictionary of dictionary)
    {
        context: {word:probability of this word given context}
    }
    data (list of lists): each list is a sentence of the text
    n(int): size of the n-gram

    Retunrs:
    prep(float): the preplexity of the model
    """
    ## FILL CODE
    perp, T = 0.0, 0
    for sentence in data:
        sentence = tuple(sentence)
        for i in range(1, len(sentence)):
            nc = min(n - 1, i)
            context = sentence[i - nc : i]
            perp += -math.log(get_prob(model, context, sentence[i]))
            T += 1
    perp = math.exp(perp / T)
    return perp


def get_proba_distrib(model, context):
    ## need to get the the words after the context and their probability of appearance
    ## after this context
    """
    Parameters:
    model (dictionary of dictionary)
    {
        context: {word:probability of this word given context}
    }
    context (list of strings): the sentence we need to find the words after it and
    thier probabilites

    Retunrs:
    words_and_probs(dic): {word: probability of word given context}

    """
    # code a recursive function over context
    # to find the longest available ngram

    ## FILL CODE

    if context in model:
        return model[context]
    else:
        return get_proba_distrib(model, context[1:])


def finish_sentence(model):
    """
    Parameters:
    model (dictionary of dictionary)
    {
        context: {word:probability of this word given context}
    }

    Retunrs:
    sentence (list of strings): a sentence sampled according to the language model.


    """
    # generate a sentence. A sentence starts with a <s> and ends with a </s>
    # Possiblly a use function is:
    # np.random.choice(x, 1, p = y)

    # where x is a list of things to sample from
    # and y is a list of probability (of the same length as x)
    sentence = ["<s>"]
    while sentence[-1] != "</s>" and len(sentence) < 11:
        ## FILL CODE
        proba = get_proba_distrib(model, tuple(sentence))
        w = np.random.choice((list(proba.keys())), 1, p=list(proba.values()))
        sentence.append(w[0])
    return sentence


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
    sentence = ["she", "was", "not"]
    n = 3
    corpus = nltk.word_tokenize(nltk.corpus.gutenberg.raw("austen-sense.txt").lower())
    randomize = False
    print(finish_sentence())
