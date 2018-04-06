
from .Type import Type

class TypeAlias(Type):
    def __init__(self, api, identifier, aliasedType):
        super(TypeAlias, self).__init__(api, identifier)
        self.aliasedType = aliasedType
