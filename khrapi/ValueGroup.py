
from .Type import Type;

class ValueGroup(Type):
    def __init(self, identifier):
        super(Type, self).__init__(identifier)
        self.values = []
