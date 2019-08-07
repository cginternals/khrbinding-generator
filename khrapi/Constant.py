
class Constant(object):
    def __init__(self, api, identifier, value):
        self.api = api
        self.identifier = identifier # self.name?
        self.value = value if value is not None else "__TODO_INVALID_VALUE__"
        self.groups = []
        self.type = None
        self.generic = False

    def __lt__(self, other):
        return self.identifier < other.identifier