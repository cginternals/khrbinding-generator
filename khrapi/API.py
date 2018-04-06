
# from .Version import Version;
# from .Extension import Extension;

class API(object):
    def __init__(self, identifier):
        self.identifier = identifier
        self.versions = []
        self.extensions = []
        self.types = []
        self.functions = []
        self.constants = []
        self.dependencies = []

    def constantByIdentifier(self, identifier):
        return next((c for c in self.constants if c.identifier == identifier), None)

    def functionByIdentifier(self, identifier):
        return next((f for f in self.functions if f.identifier == identifier), None)

    def typeByIdentifier(self, identifier):
        return next((t for t in self.types if t.identifier == identifier), None)

    def functionByIdentifier(self, identifier):
        return next((f for f in self.functions if f.identifier == identifier), None)

    def extensionByIdentifier(self, identifier):
        return next((e for e in self.extensions if e.identifier.endswith(identifier)), None)