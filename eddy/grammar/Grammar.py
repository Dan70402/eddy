import nltk
import re


class Grammar():

    def __init__(self, str):
        self.grammar = self._getGrammarFromString(str)
        self.tags = self._getTagsFromString(str)

    def _getGrammarFromString(self, str):
        return nltk.CFG.fromstring(str)

    def _getTagsFromString(self, str):
        reg = re.compile("^'[a-zA-Z]+'")
        tags = []
        for t in str.split():
            if reg.match(t):
                if t not in tags:
                    tags.append(t.translate(None, "'"))
        return tags