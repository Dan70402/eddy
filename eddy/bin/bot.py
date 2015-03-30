from eddy.module.action import ActionEvent
from eddy.module.query import QueryEvent
from eddy.parser import Parser

parser = Parser.Parser()
#action = ActionEvent.ActionEvent(parser)
action =QueryEvent.QueryEvent(parser)
print 'Eddy>> What would you like?'
print 'Eddy>> You can say \'invite @dan to room\'...'
while True:
    try:
        var = raw_input("user>> ")
        response = action.find(var)
        if response.result:
            print 'Eddy>> ' + str(response.data)
        else:
            print "Huh?"
    except Exception, ex:
        print ex