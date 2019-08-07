
from .FeatureSet import FeatureSet

class Version(FeatureSet):
    def __init__(self, api, identifier, versionString):
        identifier = "".join([c for c in identifier if not c.isdigit() ] + [ c for c in versionString if c.isdigit() ])
        super(Version, self).__init__(api, identifier)
        self.majorVersion, self.minorVersion = [ int(val) for val in versionString.split(".")[0:2] ]
        self.isCore = False
        self.isExt = False
        self.deprecatedFunctions = []
        self.deprecatedConstants = []
        self.deprecatedTypes = []
        self.removedFunctions = []
        self.removedConstants = []
        self.removedTypes = []
