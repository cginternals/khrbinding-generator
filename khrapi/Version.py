
from .FeatureSet import FeatureSet

class Version(FeatureSet):
    def __init__(self, api, identifier, versionString):
        super(Version, self).__init__(api, identifier)
        self.majorVersion, self.minorVersion = [ int(val) for val in versionString.split(".")[0:2] ]
        self.pathVersion = 0
        self.deprecatedFunctions = []
        self.deprecatedConstants = []
        self.deprecatedTypes = []
        self.removedFunctions = []
        self.removedConstants = []
        self.removedTypes = []
