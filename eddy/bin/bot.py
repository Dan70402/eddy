from eddy.module.action import ActionEvent
from eddy.parser import Parser

parser = Parser.Parser()
action = ActionEvent.ActionEvent(parser)
print 'Eddy>> What would you like?'
print 'Eddy>> You can say \'invite @dan to room\'...'
while True:
    try:
        var = raw_input("user>> ")
        response = action.findAction(var)
        if response.result:
            print 'Eddy>> ' + str(response.data)
        else:
            print "Huh?"
    except Exception, ex:
        print ex