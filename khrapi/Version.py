
from .FeatureSet import FeatureSet

class Version(FeatureSet):
    def __init__(self, api, identifier, versionString):
        super(Version, self).__init__(api, identifier)
        self.majorVersion = 0
        self.minorVersion = 0
        self.pathVersion = 0
        self.deprecatedFunctions = []
        self.deprecatedConstants = []
        self.deprecatedTypes = []
        self.removedFunctions = []
        self.removedConstants = []
        self.removedTypes = []
