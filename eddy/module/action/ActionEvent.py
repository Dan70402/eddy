import nltk
from eddy import logger

class ActionEvent():
    def __init__(self, parser):
        self._parser = parser

        self._action_type = None
        self._action_target = None
        self._action_verb = None
        self._to = None
        self._named_noun = None

        self._result = EventResponse(self.__class__.__name__)

        #@TODO parse directly from grammar?
        self._tokens = [
            'S/NP', 'NP', 'VP', 'EML', 'PP', 'NNP',
            'N', 'V', 'DT', 'TO', 'IN', 'VB', 'P'
        ]

#S -> N | N 'EML' | N 'EML' PP | N 'EML' PP PP
        self._grammar = nltk.CFG.fromstring("""
S -> S/NP | S/NP NNP | S/NP NNP PP | S/NP NNP PP PP
S -> NP VP | NP VP NNP | NP VP NNP PP | NP VP NNP PP PP
S/NP -> VP
NP -> N | Det N
NNP -> 'EML' | 'USR'
VP -> V | V NP | V PP | V NP PP | V PP NP
Det -> 'DT'
PP -> P NP
P -> 'TO' | 'IN'
V -> 'VB'
N -> 'NN'
""")

    def findInvite(self, sentence):
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
                        if subtree.label() == 'NP':
                            if not self._named_noun:
                                if map.has_key('NN'):
                                    self._named_noun = map['NN'].pop(0)

                        if subtree.label() == 'VP' or subtree.label() == 'V':
                            if not self._action_verb:
                                if map.has_key('VB'):
                                    self._action_verb = map['VB'].pop(0)

                            if subtree.label() == 'VP':
                                for child in subtree:
                                    #only occurs in the second node at depth S
                                    #VP can tree to VP->V VP->V NP
                                    if type(child) is nltk.Tree:
                                        if child.label() == 'NP':
                                            if not self._action_type:
                                                self._action_type = map['NN'].pop(0)
                                        if child.label() == 'PP':
                                            leaf = child.leaves().pop(0)
                                            if leaf == 'TO':
                                                #'TO' preposition indicates destination
                                                if not self._action_target:
                                                    self._action_target = map['NN'].pop(0)
                                            if leaf == 'IN':
                                                #'IN' preposition indicates the type
                                                if not self._action_type:
                                                    self._action_type = map['NN'].pop(0)

                        if subtree.label() == 'S/NP':
                            #get the first VB first NN and first EML
                            #only occurs in the first node at depth S
                            for child in tree[0][0]:
                                #S/NP can tree to VP->NP PP, VP->PP
                                if child.label() == 'NP':
                                    if not self._action_type:
                                        self._action_type = map['NN'].pop(0)
                                if child.label() == 'PP':
                                    if not self._action_target:
                                        self._action_target = map['NN'].pop(0)

                            if map.has_key('VB'):
                                self._action_verb = map['VB'].pop(0)

                        if subtree.label() == 'PP':
                            leaf = subtree[0].leaves().pop()
                            if leaf == 'TO':
                                #'TO' preposition indicates destination
                                if not self._action_target:
                                    self._action_target = map['NN'].pop(0)
                            if leaf == 'IN':
                                #'IN' preposition indicates the type
                                if not self._action_type:
                                    self._action_type = map['NN'].pop(0)

                        if subtree.label() == 'NNP':
                            if not self._to:
                                leaf = subtree[0]
                                if map.has_key(leaf):
                                    #@TODO add POS to return (useful for distinguishing USR\EML
                                    self._to = map[leaf].pop(0)

                logger.debug('action_type:'+str(self._action_type)+' verb:'+str(self._action_verb)+' to:'+str(self._to)+' action_target:'+str(self._action_target))
                self._result.result = True

        return self._getResult()


    def _mapBack(self, leaves, lookup_dict):
        index_counter = {}
        result = {}
        for tag in lookup_dict.keys():
            index_counter[tag] = 0
            result[tag] = []

        for l in leaves:
            result[l].append(lookup_dict[l][index_counter[l]])
            index_counter[l] += 1

        return result

    def _getResult(self):
        data = {
            "type" : self._action_type,
            "target" : self._action_target,
            "verb" : self._action_verb,
            "to" : self._to,
            "named" : self._named_noun
        }
        self._result.data = data
        return self._result

    def _clearState(self):
        self._action_type = None
        self._action_target = None
        self._action_verb = None
        self._to = None
        self._named_noun = None
        self._result.result = False

class EventResponse():
    def __init__(self, event, data=None, result=False):
        self.event = event
        if data:
            self.data = data
        else:
            self.data = {}
        self.result = result