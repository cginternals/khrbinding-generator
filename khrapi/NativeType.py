
from .Type import Type

class NativeType(Type):
    def __init__(self, identifier):
        super(Type, self).__init__(identifier)
        self.declaration = None
