import nltk
import os
import pickle
from eddy.util import Wrapper


class SequentialTagger(Wrapper.Wrapper):
    def __init__(self, corpus=nltk.corpus.nps_chat):
        tagger = self._loadTagger(corpus)
        super(SequentialTagger,self).__init__(obj=tagger)

    def _loadTagger(self, corpus):
        pickle_file = os.path.dirname(os.path.realpath(__file__)) + '/' + self.__class__.__name__ + '.p'
        if os.path.isfile(pickle_file):
            with open(pickle_file, 'rb') as f:
                t3 = pickle.load(f)
        else:
            tagged_posts = corpus.tagged_posts()
            t0 = nltk.DefaultTagger('NN')
            t1 = nltk.UnigramTagger(tagged_posts, backoff=t0)
            t2 = nltk.BigramTagger(tagged_posts, backoff=t1)

            #Email Tagger
            regexps = [
                (r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",'EML'), #Emails
                (r"(^@[a-zA-Z0-9_]+$)",'USR'), #Mentions (Users)
            ]
            t3 = nltk.RegexpTagger(regexps=regexps, backoff=t2)

            # with open(pickle_file, 'wb') as f:
            #     pickle.dump(t3, f)

        return t3