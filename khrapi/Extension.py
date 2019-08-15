
from .FeatureSet import FeatureSet

class Extension(FeatureSet):
    
    def __init__(self, api, identifier, platform = ""):
        super(Extension, self).__init__(api, identifier)
        self.platform = platform

    def __lt__(self, other):
        return self.identifier < other.identifier
