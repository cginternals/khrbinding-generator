
from .Type import Type

class NativeType(Type):
    def __init__(self, api, identifier, declaration):
        super(NativeType, self).__init__(api, identifier)
        self.declaration = declaration

    def getDeclaration(self):
        return self.declaration
