import unittest
from eddy.parser import Parser
from eddy.module.invite.InviteEvent import InviteEvent


class test_InstanceDTO(unittest.TestCase):

    def setUp(self):
        self.parser = Parser.Parser()
        self.invite_event = InviteEvent(self.parser)

    def test_Tags(self):
        #['test_sent
        case_one = [#email target type verb
                    ("invite",                                      (None, None, None, 'invite')),# S/NP
                    ("invite user",                                 (None, None, 'user', 'invite')),# S/NP
                    ("invite guest",                                (None, None, 'guest', 'invite')),# S/NP
                    ("invite a user",                               (None, None, 'user', 'invite')),# S/NP
                    ("invite a guest",                              (None, None, 'guest', 'invite')),# S/NP
                    ("invite to room",                              (None, 'room', None, 'invite')),# S/NP
                    ("invite a guest to room",                      (None, 'room', 'guest', 'invite')),# S/NP
                    ("invite to room a guest",                      (None, 'room', 'guest', 'invite')),# S/NP
                    ("invite to room dan@contatta.com",             ('dan@contatta.com', 'room', None ,'invite')),# S/NP 'EML'
                    ("invite dan@contatta.com",                     ('dan@contatta.com', None, None, 'invite')),# S/NP 'EML'
                    ("invite user dan@contatta.com",                ('dan@contatta.com', None, 'user', 'invite')),# S/NP 'EML'
                    ("invite guest dan@contatta.com",               ('dan@contatta.com', None, 'guest', 'invite')),# S/NP 'EML'
                    ("invite a user dan@contatta.com",              ('dan@contatta.com', None, 'user', 'invite')),# S/NP 'EML'
                    ("invite a guest dan@contatta.com",             ('dan@contatta.com', None, 'guest', 'invite')),# S/NP 'EML'
                    ("invite user dan@contatta.com to room",        ('dan@contatta.com', 'room', 'user', 'invite')),# S/NP 'EML' PP
                    ("invite guest dan@contatta.com to room",       ('dan@contatta.com', 'room', 'guest','invite')),# S/NP 'EML' PP
                    ("invite to room dan@contatta.com as guest",    ('dan@contatta.com', 'room', 'guest', 'invite')),# S/NP 'EML' PP
                    ("invite to room dan@contatta.com as a guest",  ('dan@contatta.com', 'room', 'guest', 'invite')),# S/NP 'EML' PP
                    ("invite dan@contatta.com to room as guest",    ('dan@contatta.com', 'room', 'guest', 'invite')),#S/NP 'EML' PP PP
                    ("invite dan@contatta.com to room as a guest",  ('dan@contatta.com', 'room', 'guest', 'invite'))#S/NP 'EML' PP PP
        ]

        for sentence, correct in case_one:
            print(sentence)
            _email, _target, _type, _verb = correct
            correct_dict = {
            "email" : _email ,
            "target" : _target,
            "type" : _type,
            "verb" : _verb
            }

            result = self.invite_event.findInvite(sentence)
            self.assertDictEqual(result.data, correct_dict)

if __name__ == '__main__':
    unittest.main()
