import unittest
from eddy.parser import Parser
from eddy.module.action.ActionEvent import ActionEvent


class test_ActionEvent(unittest.TestCase):

    def setUp(self):
        self.parser = Parser.Parser()
        self.action_event = ActionEvent(self.parser)

    def test_RootSNP(self):
        #['test_sent
        SNP_case = [#named email target type verb
                    ("invite",                                      (True, None, None, None, None, 'invite')),# S/NP
                    ("invite user",                                 (True, None, None, None, 'user', 'invite')),# S/NP
                    ("invite guest",                                (True, None, None, None, 'guest', 'invite')),# S/NP
                    ("invite a user",                               (True, None, None, None, 'user', 'invite')),# S/NP
                    ("invite a guest",                              (True, None, None, None, 'guest', 'invite')),# S/NP
                    ("invite to room",                              (True, None, None, 'room', None, 'invite')),# S/NP
                    ("invite a guest to room",                      (True, None, None, 'room', 'guest', 'invite')),# S/NP
                    ("invite to room a guest",                      (True, None, None, 'room', 'guest', 'invite')),# S/NP
                    ("invite to room dan@contatta.com",             (True, None, 'dan@contatta.com', 'room', None ,'invite')),# S/NP 'EML'
                    ("invite dan@contatta.com",                     (True, None, 'dan@contatta.com', None, None, 'invite')),# S/NP 'EML'
                    ("invite user dan@contatta.com",                (True, None, 'dan@contatta.com', None, 'user', 'invite')),# S/NP 'EML'
                    ("invite guest dan@contatta.com",               (True, None, 'dan@contatta.com', None, 'guest', 'invite')),# S/NP 'EML'
                    ("invite a user dan@contatta.com",              (True, None, 'dan@contatta.com', None, 'user', 'invite')),# S/NP 'EML'
                    ("invite a guest dan@contatta.com",             (True, None, 'dan@contatta.com', None, 'guest', 'invite')),# S/NP 'EML'
                    ("invite user dan@contatta.com to room",        (True, None, 'dan@contatta.com', 'room', 'user', 'invite')),# S/NP 'EML' PP
                    ("invite guest dan@contatta.com to room",       (True, None, 'dan@contatta.com', 'room', 'guest','invite')),# S/NP 'EML' PP
                    ("invite to room dan@contatta.com as guest",    (True, None, 'dan@contatta.com', 'room', 'guest', 'invite')),# S/NP 'EML' PP
                    ("invite to room dan@contatta.com as a guest",  (True, None, 'dan@contatta.com', 'room', 'guest', 'invite')),# S/NP 'EML' PP
                    ("invite dan@contatta.com to room as guest",    (True, None, 'dan@contatta.com', 'room', 'guest', 'invite')),#S/NP 'EML' PP PP
                    ("invite dan@contatta.com to room as a guest",  (True, None, 'dan@contatta.com', 'room', 'guest', 'invite')),#S/NP 'EML' PP PP
        ]
    
        for sentence, correct in SNP_case:
            _result, _named, _to, _target, _type, _verb = correct
            correct_dict = {
                "type" : _type,
                "target" : _target,
                "verb" : _verb,
                "to" : _to,
                "named" : _named
            }

            result = self.action_event.findInvite(sentence)
            self.assertDictEqual(result.data, correct_dict)
            self.assertEqual(result.result, _result)
    
    def test_RootNP(self):
        #['test_sent
        NP_case = [#email target type verb
                    ("Eddy invite",                                      (True, 'Eddy', None, None, None, 'invite')),# NP VP
                    ("Eddy invite user",                                 (True, 'Eddy', None, None, 'user', 'invite')),# NP VP
                    ("Eddy invite guest",                                (True, 'Eddy', None, None, 'guest', 'invite')),# NP VP
                    ("Eddy invite a user",                               (True, 'Eddy', None, None, 'user', 'invite')),# NP VP
                    ("Eddy invite a guest",                              (True, 'Eddy', None, None, 'guest', 'invite')),# NP VP
                    ("Eddy invite to room",                              (True, 'Eddy', None, 'room', None, 'invite')),# NP VP
                    ("Eddy invite a guest to room",                      (True, 'Eddy', None, 'room', 'guest', 'invite')),# NP VP
                    ("Eddy invite to room a guest",                      (True, 'Eddy', None, 'room', 'guest', 'invite')),# NP VP
                    ("Eddy invite to room dan@contatta.com",             (True, 'Eddy', 'dan@contatta.com', 'room', None ,'invite')),# NP VP 'EML'
                    ("Eddy invite dan@contatta.com",                     (True, 'Eddy', 'dan@contatta.com', None, None, 'invite')),# N VP 'EML'
                    ("Eddy invite user dan@contatta.com",                (True, 'Eddy', 'dan@contatta.com', None, 'user', 'invite')),# N VP 'EML'
                    ("Eddy invite guest dan@contatta.com",               (True, 'Eddy', 'dan@contatta.com', None, 'guest', 'invite')),# N VP 'EML'
                    ("Eddy invite a user dan@contatta.com",              (True, 'Eddy', 'dan@contatta.com', None, 'user', 'invite')),# N VP 'EML'
                    ("Eddy invite a guest dan@contatta.com",             (True, 'Eddy', 'dan@contatta.com', None, 'guest', 'invite')),# N VP 'EML'
                    ("Eddy invite user dan@contatta.com to room",        (True, 'Eddy', 'dan@contatta.com', 'room', 'user', 'invite')),# N VP 'EML' PP
                    ("Eddy invite guest dan@contatta.com to room",       (True, 'Eddy', 'dan@contatta.com', 'room', 'guest','invite')),# N VP 'EML' PP
                    ("Eddy invite to room dan@contatta.com as guest",    (True, 'Eddy', 'dan@contatta.com', 'room', 'guest', 'invite')),# N VP 'EML' PP
                    ("Eddy invite to room dan@contatta.com as a guest",  (True, 'Eddy', 'dan@contatta.com', 'room', 'guest', 'invite')),# N VP 'EML' PP
                    ("Eddy invite dan@contatta.com to room as guest",    (True, 'Eddy', 'dan@contatta.com', 'room', 'guest', 'invite')),# N VP 'EML' PP PP
                    ("Eddy invite dan@contatta.com to room as a guest",  (True, 'Eddy', 'dan@contatta.com', 'room', 'guest', 'invite')),# N VP 'EML' PP PP
        ]
    
        for sentence, correct in NP_case:
            _result, _named, _to, _target, _type, _verb = correct
            correct_dict = {
                "type" : _type,
                "target" : _target,
                "verb" : _verb,
                "to" : _to,
                "named" : _named
            }

            result = self.action_event.findInvite(sentence)
            self.assertDictEqual(result.data, correct_dict)
            self.assertEqual(result.result, _result)

    def test_InviteNoun(self):
        #['test_sent
        Noun_case = [#email target type verb
                    ("send an invite",                                  (True, None, None, None, 'invite', 'send')),# N VP
                    ("send a guest invite",                             (False, None, None, None, None, None)),#
                    ("send dan@contatta.com a guest invite",            (False, None, None, None, None, None)),#
                    ("send an invite to dan@contatta.com",              (False, None, None, None, None, None)),#
                    ("send a guest invite to dan@contatta.com",         (False, None, None, None, None, None)),#
                    ("Eddy send an invite",                             (True, 'Eddy', None, None, 'invite', 'send')),# N VP
                    ("Eddy send a guest invite",                        (False, None, None, None, None, None)),#
                    ("Eddy send dan@contatta.com a guest invite",       (False, None, None, None, None, None)),#
                    ("Eddy send an invite to dan@contatta.com",         (False, None, None, None, None, None)),#
                    ("Eddy send a guest invite to dan@contatta.com",    (False, None, None, None, None, None)),#
        ]

        for sentence, correct in Noun_case:
            _result, _named, _to, _target, _type, _verb = correct
            correct_dict = {
                "type" : _type,
                "target" : _target,
                "verb" : _verb,
                "to" : _to,
                "named" : _named
            }

            result = self.action_event.findInvite(sentence)
            self.assertDictEqual(result.data, correct_dict)
            self.assertEqual(result.result, _result)

            result = self.action_event.findInvite(sentence)
            self.assertDictEqual(result.data, correct_dict)
            self.assertEqual(result.result, _result)


if __name__ == '__main__':
    unittest.main()
