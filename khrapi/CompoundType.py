
from .Type import Type

class CompoundType(Type):
    def __init__(self, identifier):
        super(CompoundType, self).__init__(identifier)
        self.memberFunctions = []
        self.staticFunctions = []
        self.memberAttributes = []
        self.staticAttributes = []
