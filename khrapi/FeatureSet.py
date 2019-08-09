
class FeatureSet(object):
    def __init__(self, api, identifier):
        self.api = api
        self.identifier = identifier
        self.supportedAPIs = []
        self.requiredExtensions = []
        self.requiredFunctions = []
        self.requiredConstants = []
        self.requiredTypes = []

    def __lt__(self, other):
        return self.identifier < other.identifier
