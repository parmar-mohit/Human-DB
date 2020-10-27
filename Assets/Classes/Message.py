from pickle import dumps


class Message:
    def __init__(self, type, action, info, request):
        self.type = type
        self.action = action
        self.info = info
        self.request = request

    def encode(self):
        return dumps(self)
