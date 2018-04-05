
from .Type import Type;

class ValueGroup(Type):
    def __init(self, identifier):
        super(ValueGroup, self).__init__(identifier)
        self.values = []
