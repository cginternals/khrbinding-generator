
from .FeatureSet import FeatureSet

class Version(FeatureSet):
    def __init__(self, api, internalIdentifier, identifier, versionString, apiString):
        super(Version, self).__init__(api, internalIdentifier)
        self.apiIdentifier = identifier
        self.apiString = apiString
        self.majorVersion, self.minorVersion = [ int(val) for val in versionString.split(".")[0:2] ]
        self.isCore = False
        self.isExt = False
        self.deprecatedFunctions = []
        self.deprecatedConstants = []
        self.deprecatedTypes = []
        self.removedFunctions = []
        self.removedConstants = []
        self.removedTypes = []

    def __lt__(self, other):
        return self.majorVersion < other.majorVersion or (self.majorVersion == other.majorVersion and self.minorVersion < other.minorVersion)
