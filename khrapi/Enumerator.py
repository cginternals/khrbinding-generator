
from .ValueGroup import ValueGroup

class Enumerator(ValueGroup):
    def __init__(self, api, identifier):
        super(Enumerator, self).__init__(api, identifier)
        self.unsigned = True

    def __lt__(self, other):
        return self.identifier < other.identifier
