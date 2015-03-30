from eddy.module.action import ActionEvent
from eddy.module.query import QueryEvent
from eddy.parser import Parser

parser = Parser.Parser()
events = [
    ActionEvent.ActionEvent(parser),
    QueryEvent.QueryEvent(parser)
]
print 'Eddy>> What would you like?'
print 'Eddy>> You can say \'invite @dan to room\'...'
while True:
    try:
        var = raw_input("user>> ")
        responded = False
        for e in events:
            response = e.find(var)
            if response.result:
                print 'Eddy>> I found event:' + str(response.event) + ' with ' + str(response.data)
                responded = True
                break
        if not responded:
            print "Huh?"
    except Exception, ex:
        print ex