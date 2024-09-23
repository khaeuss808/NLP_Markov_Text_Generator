import nltk
from collections import defaultdict

def finish_sentence(sentence, n, corpus, randomize=False):
    """this is actually building our sentence"""
    sentence_ans = list(sentence)
    ngram = tuple(sentence[len(sentence) - n + 1 :]) 
    allngram_dict= create_big_dict_ngrams(corpus, n, ngram)

    while len(sentence_ans) < 10 or sentence_ans[-1] not in [".", "?", "!"]:
          
    return sentence_ans



def create_big_dict_ngrams(my_corpus, my_n, my_nrgram):
    allngram_nestedDict = defaultdict(lambda: defaultdict(int))
    ngram_redux = list(my_nrgram)
    my_n -=1
    while len(ngram_redux) >=0: #while there is still ngram left to consider

        allngram_nestedDict[ngram_redux] = {}

        if len(ngram_redux) ==0:
            for everyword in my_corpus:
                 for i in range(len(my_corpus)):
                    if my_corpus[i] == everyword:
                         allngram_nestedDict[ngram_redux][everyword] +=1
        else:
            for everyword in my_corpus:
                for i in range (len(my_corpus)):
                    if my_corpus[i:i+my_n-1] == ngram_redux and my_corpus[i+my_n-1]==everyword:
                        allngram_nestedDict[ngram_redux][everyword] +=1

        ngram_redux.pop(0)
        my_n -= 1

    
          




    for (each_word) in (corpus):  # if the word follows the ngram then add it to the dict and add 1
                for i in range(len(corpus)):
                    if (
                        corpus[i : i + n - 2] == ngram
                        and corpus[i + n - 1] == each_word
                    ):
                        poss_nextword_dict[each_word] += 1
                    pass
                pass
            pass 

if __name__ == "__main__":

