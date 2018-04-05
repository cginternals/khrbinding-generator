
from .Type import Type

class Function(Type):
    def __init__(self, identifier):
        super(Function, self).__init__(identifier)
        self.returnType = None
        self.parameters = []
