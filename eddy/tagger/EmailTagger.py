import nltk
from eddy.util import Wrapper

class EmailTagger(Wrapper.Wrapper):
    def __init__(self, backoff=None):
        regex = [(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",'EML')]
        super(EmailTagger,self).__init__(obj=nltk.RegexpTagger(regexps=regex, backoff=backoff))