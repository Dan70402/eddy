class AbstractEvent:

    def find(self, sentence):
        raise NotImplementedError()

    def _mapBack(self, leaves, lookup_dict):
        """
        Used to map back a POS tag to the value it represents

        :param leaves:
        :param lookup_dict:
        :return:
        """
        index_counter = {}
        result = {}
        for tag in lookup_dict.keys():
            index_counter[tag] = 0
            result[tag] = []

        for l in leaves:
            result[l].append(lookup_dict[l][index_counter[l]])
            index_counter[l] += 1

        return result