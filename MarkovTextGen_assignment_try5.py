import nltk
from collections import defaultdict


def finish_sentence(sentence, n, corpus, randomize=False):
    """this is actually building our sentence"""
    sentence_ans = list(sentence)
    ngram = tuple(sentence[len(sentence) - n + 1 :])
    allngram_dict = dict_ofngrams_and_probs(corpus, n, ngram)
    my_corpus = list(corpus)

    while len(sentence_ans) < 10 and sentence_ans[-1] not in [".", "?", "!"]:
        next_word = nextword(allngram_dict, ngram)
        next_word = "".join(next_word)
        sentence_ans.append(next_word)

        ngram = tuple(sentence_ans[len(sentence_ans) - n + 1 :])

    return sentence_ans


def dict_ofngrams_and_probs(my_corpus, my_n, my_ngram):
    # build_ngram
    total_number_words = 0
    frequencies = defaultdict(lambda: defaultdict(lambda: 0.0))
    for i in range(len(my_corpus)):
        total_number_words += 1
        for k in range(my_n):
            if i - k < 0:
                break
            frequencies[tuple(my_corpus[i - k : i])][tuple(my_corpus[i])] += 1
            # print(frequencies)
    # print frequencies
    nonalpha_probs = defaultdict(lambda: defaultdict(lambda: 0.0))
    for context in frequencies.keys():
        denom = 0
        for w in frequencies[context].keys():
            denom += frequencies[context][w]
        for w in frequencies[context].keys():
            nonalpha_probs[context][w] = frequencies[context][w] / denom

    return nonalpha_probs


def nextword(dictionary_frequency, ngram):
    ngram_dict = {}
    if ngram in dictionary_frequency:
        ngram_dict = dictionary_frequency[ngram]
        print(ngram_dict)
        max_probword = max(ngram_dict, key=ngram_dict.get)
        # look at this again
    else:
        max_probword = stupid_backoff(dictionary_frequency, ngram)

    return max_probword


def stupid_backoff(dictionary_frequency, ngram):
    stupid_ngram = ngram[1:]
    allword_maxprobs = {}

    alpha_expo = 1
    # search for the smaller ngram
    while len(stupid_ngram) > 0:
        if stupid_ngram in dictionary_frequency:
            stupid_ngram_dict = dictionary_frequency[stupid_ngram]
            stupid_maxword = max(stupid_ngram_dict, key=stupid_ngram_dict.get)
            # need to consider alpha here
            allword_maxprobs[stupid_maxword] = stupid_ngram_dict[stupid_maxword] * (
                0.4**alpha_expo
            )

        stupid_ngram.pop(0)
        alpha_expo += 1

    # if len(stupid_ngram)==0: maybe we dont need this
    # then unigram

    return max(allword_maxprobs, key=allword_maxprobs.get)


if __name__ == "__main__":
    sentence = ["she", "was", "not"]
    n = 3
    corpus = [
        "she",
        "was",
        "not",
        "going",
        "to",
        "the",
        "class",
        "at",
        "least",
        "not",
        "with",
        "the",
        "dog",
        ".",
        "this",
        "was",
        "not",
        "the",
        "best",
        "plan",
        "because",
        "michael",
        "was",
        "not",
        "going",
        "with",
        "his",
        "cat",
        "too",
    ]
    randomize = False
    print(finish_sentence(sentence, n, tuple(corpus), randomize))
