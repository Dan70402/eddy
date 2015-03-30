import nltk
from eddy import logger
from eddy.grammar import Grammar
from eddy.module.AbstractEvent import AbstractEvent
from eddy.module.EventReponse import EventResponse

class QueryEvent(AbstractEvent):

    def __init__(self, parser):
        self._parser = parser

        self._search_phrase = None
        self._named_noun = None

        self._result = EventResponse(self.__class__.__name__)

        #@TODO proof of concept for query... likely separate out into multipl question types and possession cases
        self._grammar = Grammar.Grammar("""
S -> QP VP | QP NP
QP -> 'WRB' | 'WRB' P | 'WRB' 'MD' 'PRP' | 'WRB' 'VBP' 'PRP'
NP -> N | Det N
VP -> V | V NP | V PP | V NP PP | V PP NP
Det -> 'DT'
PP -> P NP
P -> 'TO' | 'IN' | 'PRP$'
V -> 'VB' | 'VBZ'
N -> 'NN'
""")

    def find(self, sentence):
        logger.debug("Processing: '" + sentence + "'")
        self._clearState()
        trees, lookup_dict = self._parser.parse(self._grammar, sentence)
        if trees:
            for tree in trees:
                #tree.draw()

                leaves = tree.leaves()
                map = self._mapBack(leaves, lookup_dict)

                for subtree in tree:
                    if type(subtree) is nltk.Tree:
                        #We can determine our values by traversing the depth 1 branches
                        if subtree.label() == 'VP' or subtree.label() == 'NP':
                            leaves = subtree.leaves()
                            values = []
                            if not self._search_phrase:
                                for l in leaves:
                                    values.append(map[l].pop(0))
                                self._search_phrase = ' '.join(values)

                logger.info('names_noun:' + str(self._named_noun) + ' search_phrase:' + str(self._search_phrase))
                self._result.result = True

        return self._getResult()




    def _getResult(self):
        """
        Helper to build the results
        :return:
        """
        data = {
            "phrase" : self._search_phrase,
            "named" : self._named_noun
        }
        self._result.data = data
        return self._result

    def _clearState(self):
        """
        Clear the result state of this object.  You shouldn't instantiate
        this class everytime you need to parse a string... just call the
        classes find()
        :return:
        """
        self._search_phrase = None
        self._named_noun = None
        self._result.result = False