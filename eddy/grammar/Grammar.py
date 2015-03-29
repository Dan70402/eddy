import nltk
import re


class Grammar():

    def __init__(self, str):
        self.grammar = self._getGrammarFromString(str)
        self.tags = self._getTagsFromString(str)

    def _getGrammarFromString(self, str):
        """
        Get nltk grammar object froms tring

        :param str:
        :return:
        """
        return nltk.CFG.fromstring(str)

    def _getTagsFromString(self, str):
        """
        Build a list of POS tags used from a grammar string.
        Can be used to validate that a grammar can process
        incoming POS tags

        :param str:
        :return:
        """
        reg = re.compile("^'[a-zA-Z]+'")
        tags = []
        for t in str.split():
            if reg.match(t):
                if t not in tags:
                    tags.append(t.translate(None, "'"))
        return tags