from eddy.parser import Parser
from eddy.module.invite.InviteEvent import InviteEvent
from eddy import logger

runner = Parser.Parser()

case_one = [
    "invite",# S/NP
    "invite user",# S/NP
    "invite guest",# S/NP
    "invite a user",# S/NP
    "invite a guest",# S/NP
    "invite to room",# S/NP
    "invite a guest to room",# S/NP
    "invite to room a guest",# S/NP
    "invite to room dan@contatta.com",# S/NP 'EML'
    "invite dan@contatta.com",# S/NP 'EML'
    "invite user dan@contatta.com",# S/NP 'EML'
    "invite guest dan@contatta.com",# S/NP 'EML'
    "invite a user dan@contatta.com",# S/NP 'EML'
    "invite a guest dan@contatta.com",# S/NP 'EML'
    "invite user dan@contatta.com to room",# S/NP 'EML' PP

    "invite guest dan@contatta.com to room",# S/NP 'EML' PP
    "invite to room dan@contatta.com as guest",# S/NP 'EML' PP
    "invite to room dan@contatta.com as a guest",# S/NP 'EML' PP
    "invite dan@contatta.com to room as guest",#S/NP 'EML' PP PP
    "invite dan@contatta.com to room as a guest"#S/NP 'EML' PP PP
]

parser = Parser.Parser()
invite_event = InviteEvent(parser)
for case in case_one:
    result = invite_event.findInvite(case)
    if not result:
        logger.error("BAD")




invite_examples = [
#1:1 context
	"invite dan@contatta.com",# S/NP
	"Eddy invite",# NP VP
	"Eddy invite user",# NP VP
	"Eddy invite a user",# NP VP
	"Eddy invite dan@contatta.com",# NP VP 'EML'
	"Eddy invite user dan@contatta.com",# NP VP 'EML'
	"Eddy invite guest dan@contatta.com",# NP VP 'EML'
	"Eddy invite dan@contatta.com to PLACE",# NP VP 'EML' NP
	"Eddy invite dan@contatta.com to PLACE as user",# NP VP 'EML NP PP
	"Eddy invite dan@contatta.com to PLACE as guest",# NP VP 'EML NP PP
	"Eddy invite dan@contatta.com to PLACE as a user",# NP VP 'EML NP PP
	"Eddy invite dan@contatta.com to PLACE as a guest",# NP VP 'EML NP PP
	"Eddy invite dan@contatta.com as user",# NP VP 'EML' PP
	"Eddy invite dan@contatta.com as guest",# NP VP 'EML' PP
	"Eddy invite dan@contatta.com as a user",# NP VP 'EML' PP
	"Eddy invite dan@contatta.com as a guest",# NP VP 'EML' PP
	"Eddy invite dan@contatta.com as user to PLACE",# NP VP 'EML' PP NP
	"Eddy invite dan@contatta.com as guest to PLACE",# NP VP 'EML' PP NP
	"Eddy invite user dan@contatta.com to PLACE",# NP VP 'EML' NP
	"Eddy invite guest dan@contatta.com to PLACE",# NP VP 'EML' NP
]
# #room context
# 	"Eddy invite dan@contatta.com to room",# NP VP 'EML' NP
# 	"Eddy invite dan@contatta.com to the room",# NP VP 'EML' NP
# 	"Eddy invite dan@contatta.com as user",# NP VP 'EML' PP
# 	"Eddy invite dan@contatta.com as guest",# NP VP 'EML' PP
# 	"Eddy invite dan@contatta.com as a user",# NP VP 'EML' PP
# 	"Eddy invite dan@contatta.com as a guest",# NP VP 'EML' PP
# 	"Eddy invite dan@contatta.com as a user to room",
# 	"Eddy invite dan@contatta.com as a guest to room",
# 	"Eddy invite dan@contatta.com as a user to the room",
# 	"Eddy invite dan@contatta.com as a guest to the room",
# 	"Eddy invite dan@contatta.com to room as user",
# 	"Eddy invite dan@contatta.com to room as guest",
# 	"Eddy invite dan@contatta.com to the room as user",
# 	"Eddy invite dan@contatta.com to the room as guest",

#same use cases as above but invitation as noun isntead of invite verb
send_examples = [
	"Eddy send invite",
	"Eddy send invitation",
	"Eddy send user invite",
	"Eddy send user invitation",
	"Eddy send guest invite"
	"Eddy send guest invitation",
	"Eddy send invite to Dan",
	"Eddy send invitation to Dan",
	"Eddy send guest invite to dan@contatta.com",
	"Eddy send guest invitation to dan@contatta.com",
	"Eddy send user invite to dan@contatta.com",
	"Eddy send user invitation to dan@contatta.com",
]
#
