import nltk
from eddy import logger

class InviteEvent():
    def __init__(self, parser):
        self._parser = parser

        self._invite_type = None
        self._invite_target = None
        self._invite_verb = None
        self._invite_email = None

        result = {
            "type" : self._invite_type,
            "target" : self._invite_target,
            "verb" : self._invite_verb,
            "email" : self._invite_email
        }
        self._result = EventResponse(self.__class__.__name__, data=result)

#S -> N | N 'EML' | N 'EML' PP | N 'EML' PP PP
        self._grammar = nltk.CFG.fromstring("""
S -> S/NP | S/NP 'EML' | S/NP 'EML' PP | S/NP 'EML' PP PP
S/NP -> VP
NP -> N | Det N
VP -> V | V NP | V PP | V NP PP | V PP NP
Det -> 'DT'
PP -> P NP
P -> 'TO' | 'IN'
V -> 'VB'
N -> 'NN'
""")

    def findInvite(self, sentence):
        trees, lookup_dict = self._parser.parse(self._grammar, sentence)
        if trees:
            for tree in trees:
                #tree.draw()

                action_type = None
                action_target = None
                verb = None
                email = None

                leaves = tree.leaves()
                map = self._mapBack(leaves, lookup_dict)

                for subtree in tree:
                    if type(subtree) is nltk.Tree:
                        #We can determine our values by traversing the depth 1 branches
                        if subtree.label() == 'S/NP':
                            #get the first VB first NN and first EML
                            for child in tree[0][0]:
                                #S/NP can tree to VP->NP PP, VP->PP
                                if child.label() == 'NP':
                                    if not self._invite_type:
                                        self._invite_type = map['NN'].pop(0)
                                if child.label() == 'PP':
                                    if not self._invite_target:
                                        self._invite_target = map['NN'].pop(0)

                            if map.has_key('VB'):
                                self._invite_verb = map['VB'].pop(0)

                        if subtree.label() == 'PP':
                            leaf = subtree[0].leaves().pop()
                            if leaf == 'TO':
                                #'TO' preposition indicates destination
                                if not self._invite_target:
                                    self._invite_target = map['NN'].pop(0)
                                #'IN' preposition indicates the type
                                if not self._invite_type:
                                    self._invite_type = map['NN'].pop(0)
                            if leaf == 'IN':
                                if not self._invite_type:
                                    self._invite_type = map['NN'].pop(0)

                    else:
                        if subtree == 'EML':
                            if not self._invite_email:
                                if map.has_key('EML'):
                                    self._invite_email = map['EML'].pop(0)


                logger.info('action_type:'+str(self._invite_type)+' verb:'+str(self._invite_verb)+' email:'+str(self._invite_email)+' action_target:'+str(self._invite_target))
                self._result.result = True

        return self._getResult()


    def _mapBack(self, leaves, lookup_dict):
        index_counter = {}
        result = {}
        for tag in lookup_dict.keys():
            index_counter[tag] = 0
            result[tag] = []

        for l in leaves:
            #print "looking up " + str(l)
            result[l].append(lookup_dict[l][index_counter[l]])
            index_counter[l] += 1

        return result

    def _getResult(self):
        data = {
            "type" : self._invite_type,
            "target" : self._invite_target,
            "verb" : self._invite_verb,
            "email" : self._invite_email
        }
        self._result.data = data
        self._clearState()
        return self._result

    def _clearState(self):
        self._invite_type = None
        self._invite_target = None
        self._invite_verb = None
        self._invite_email = None

class EventResponse():
    def __init__(self, event, data=None, result=False):
        self.event = event
        if data:
            self.data = data
        else:
            self.data = {}
        self.result = result