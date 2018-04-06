
from .Type import Type;

class ValueGroup(Type):
    def __init__(self, api, identifier):
        super(ValueGroup, self).__init__(api, identifier)
        self.values = []
