
from .Type import Type

class NativeType(Type):
    def __init__(self, identifier):
        super(NativeType, self).__init__(identifier)
        self.declaration = None
