
from .Type import Type

class Import(Type):
    def __init__(self, api, identifier, moduleName):
        super(Import, self).__init__(api, identifier)
        self.moduleName = moduleName
