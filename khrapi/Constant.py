
class Constant(object):
    def __init__(self, api, identifier, value):
        self.api = api
        self.identifier = identifier # self.name?
        self.value = value
        self.groups = []
