import random
from collections import defaultdict
import csv
import nltk


def finish_sentence(sentence, n, corpus, randomize=False):
    # create ngram which is a subset of sentence
    # while sentence <10 and not ending in punctuation

    # create the nested dictionary
    # popualte the nested dictionary with all words in the corpus, with all unique words
    #

    ngram = tuple(
        sentence[len(sentence) - n + 1 :]
    )  # make a list or change corpus one into tuple
    sentence_ans = list(sentence)
    back_off_alpha = 0.4

    while len(sentence_ans) < 10 or sentence_ans[-1] not in [".", "?", "!"]:
        if randomize == True:
            sentence_ans.append(random.choice(corpus))  # come back to this
        else:
            poss_nextword_dict = defaultdict(int)  ### probABLY WOULDNT FUCK THINGS UP
            for (
                each_word  # instead of this, we will make the below a function
            ) in (
                corpus
            ):  # if the word follows the ngram then add it to the dict and add 1
                for i in range(len(corpus)):
                    if (
                        corpus[i : i + n - 2] == ngram
                        and corpus[i + n - 1] == each_word
                    ):
                        poss_nextword_dict[each_word] += 1
                    pass
                pass
            pass
            # print(poss_nextword_dict)
            if not poss_nextword_dict:  # if the dictionary is empty
                # STUPID BACKOFF

                max_probabilities_for_each_word = {}
                n_backoff = n - 1  # wanna go ahead and backoff

                for word in corpus:
                    probability_storage = []
                    back_off_alpha_expo = 1
                    while n_backoff > 0:
                        backoff_occurence_dict = {
                            "ngram occurrences": 0,
                            "word after ngram": 0,
                        }
                        for i in range(len(corpus)):
                            if (
                                corpus[i : i + n_backoff - 2] == ngram
                                and corpus[i + n_backoff - 1] == word
                            ):
                                backoff_occurence_dict["word after ngram"] += 1
                                backoff_occurence_dict["ngram occurrences"] += 1
                            elif (
                                corpus[i : n - 2] == ngram and corpus[i + n - 1] != word
                            ):
                                backoff_occurence_dict["ngram occurrences"] += 1
                        pass

                        if (
                            backoff_occurence_dict["word after ngram"] == 0
                        ):  # the word does not appear after ngram

                            backoff_occurence_dict["ngram"] = 0
                            backoff_occurence_dict["word after ngram"] = 0
                        else:
                            probability_storage.append(
                                (backoff_occurence_dict["word after ngram"])
                                / (backoff_occurence_dict["ngram occurrences"])
                            )

                        n_backoff -= 1
                    if probability_storage:  # if it has things inside it?
                        max_probabilities_for_each_word[word] = max(
                            probability_storage
                        ) * (back_off_alpha**back_off_alpha_expo)
                    else:
                        max_probabilities_for_each_word[word] = 0
                    back_off_alpha_expo += 1

                    pass

                sentence_ans.append(
                    max(
                        max_probabilities_for_each_word,
                        key=max_probabilities_for_each_word.get,
                    )
                )

            else:  # nonstupid backoff
                sentence_ans.append(max_word(poss_nextword_dict))

            pass

        return sentence_ans


def max_word(poss_nextword_dictionary):
    probability_dict = {key: None for key in poss_nextword_dictionary}
    # put the keys of words that we see follow our ngram into a new dict

    total_ngram_occur = sum(poss_nextword_dictionary.values())

    for keys, value in poss_nextword_dictionary.items():
        probability_dict[keys] = value / total_ngram_occur
    pass

    return max(probability_dict, key=probability_dict.get)


# _____________________________________________________________________________

if __name__ == "__main__":
    test_generator()
