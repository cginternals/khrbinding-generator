
from .Type import Type

class CompoundType(Type):
    def __init__(self, api, identifier, type):
        super(CompoundType, self).__init__(api, identifier)
        self.type = type
        self.memberFunctions = []
        self.staticFunctions = []
        self.memberAttributes = []
        self.staticAttributes = []
