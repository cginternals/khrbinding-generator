
from .FeatureSet import FeatureSet

class Extension(FeatureSet):
    pass

    def __lt__(self, other):
        return self.identifier < other.identifier
