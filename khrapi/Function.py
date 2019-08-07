
from .Type import Type

class Function(Type):
    def __init__(self, api, identifier):
        super(Function, self).__init__(api, identifier)
        self.returnType = None
        self.parameters = []
        self.requiringFeatureSets = []

    def __lt__(self, other):
        return self.identifier < other.identifier
