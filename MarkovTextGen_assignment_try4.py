import nltk
from collections import defaultdict


def finish_sentence(sentence, n, corpus, randomize=False):
    """this is actually building our sentence"""
    sentence_ans = list(sentence)
    ngram = tuple(sentence[len(sentence) - n + 1 :])
    allngram_dict = dict_ofngrams_and_probs(corpus, n, ngram)
    my_corpus = list(corpus)

    while len(sentence_ans) < 10 or sentence_ans[-1] not in [".", "?", "!"]:
        probabilities = {}
        for word in corpus:
            probabilities[word] = apply_alpha_get_prob(allngram_dict, ngram, word)
        nextword = max(probabilities, key=probabilities.get)
        sentence_ans.append(nextword)
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

    nonalpha_probs = defaultdict(lambda: defaultdict(lambda: 0.0))
    for context in frequencies.keys():
        denom = 0
        for w in frequencies[context].keys():
            denom += frequencies[context][w]
        for w in frequencies[context].keys():
            nonalpha_probs[context][w] = frequencies[context][w] / denom

    return nonalpha_probs


def apply_alpha_get_prob(nonalpha_probabilitydict, context, word):
    if (
        context in nonalpha_probabilitydict
        and word in nonalpha_probabilitydict[context]
    ):
        return nonalpha_probabilitydict[context][word]
    else:
        return 0.4 * apply_alpha_get_prob(nonalpha_probabilitydict, context[1:], word)


if __name__ == "__main__":
    sentence = ["she", "was", "not"]
    n = 3
    corpus = nltk.word_tokenize(nltk.corpus.gutenberg.raw("austen-sense.txt").lower())
    randomize = False
    print(finish_sentence(sentence, n, corpus, randomize))
