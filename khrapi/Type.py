
class Type(object):
    def __init__(self, api, identifier):
        self.api = api
        self.identifier = identifier
        self.namespace = None
        self.require = None
        self.declaration = self.identifier
        self.definition = self.identifier
        self.hideDeclaration = False

    def __lt__(self, other):
        return self.identifier < other.identifier
