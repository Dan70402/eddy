class EventResponse():
    """
    Response object for an Event
    #@TODO This will be base generic class
    """
    def __init__(self, event, data=None, result=False):
        self.event = event
        if data:
            self.data = data
        else:
            self.data = {}
        self.result = result