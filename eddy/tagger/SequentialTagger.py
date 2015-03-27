import nltk
from eddy.util import Wrapper
from eddy.tagger import EmailTagger

class SequentialTagger(Wrapper.Wrapper):
    def __init__(self, corpus=nltk.corpus.nps_chat):
        tagged_posts = corpus.tagged_posts()
        t0 = nltk.DefaultTagger('NN')
        t1 = nltk.UnigramTagger(tagged_posts, backoff=t0)
        t2 = nltk.BigramTagger(tagged_posts, backoff=t1)
        t3 = EmailTagger.EmailTagger(backoff=t2)
        super(SequentialTagger,self).__init__(obj=t3)