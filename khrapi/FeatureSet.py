
class FeatureSet(object):
    def __init__(self, api, identifier):
        self.api = api
        self.identifier = identifier
        self.requiredExtensions = []
        self.requiredFunctions = []
        self.requiredConstants = []
