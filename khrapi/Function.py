
from .Type import Type

class Function(Type):
    def __init__(self, identifier):
        super(Type, self).__init__(identifier)
        self.returnType = None
        self.parameters = []
