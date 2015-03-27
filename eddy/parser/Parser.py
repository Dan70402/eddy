import nltk
from eddy.tagger import SequentialTagger
from eddy.tokenizer import TreebankTokenizer
from eddy import logger

class Parser():
    def __init__(self):
        self.tokenizer = TreebankTokenizer.TreebankTokenizer()
        self.tagger = SequentialTagger.SequentialTagger()

    def parse(self, grammar, example):
        tokens = self.tokenizer.tokenize(example)
        logger.debug("Parser tokens:" + str(tokens))
        tagged = self.tagger.tag(tokens)
        logger.debug("Parser tagged:" + str(tagged))

        pos_tags = self._genPosTags(tagged)
        lookup_dict = self._genLookupDict(tagged)

        rd_parser = nltk.RecursiveDescentParser(grammar, trace=0) #trace=2

        trees = []
        for tree in rd_parser.parse(pos_tags):
            trees.append(tree)

        return (trees, lookup_dict)

    def _genPosTags(self, tagged):
        """
        Helper to generate POS Tags for passing to grammar parser
        """
        return [pos for (token, pos) in tagged]

    def _genLookupDict(self, tagged):
        """
        Helper for mapping back POS grammar leaves to values
        """
        lookup_dict = {}
        for token,pos in tagged:
            if pos not in lookup_dict.keys():
                lookup_dict[pos] = []
            lookup_dict[pos].append(token)
        return lookup_dict
