
from .Version import Version;
from .Extension import Extension;

class API(object):
    def __init__(self, name, revision):
        self.name = name
        self.revision = revision
        self.versions = []
        self.extensions = []
        self.types = []
        self.functions = []
        self.constants = []
        self.declarations = []
        self.dependencies = []
        self.vendors = []

    def constantByIdentifier(self, identifier):
        return next((c for c in self.constants if c.identifier == identifier), None)

    def functionByIdentifier(self, identifier):
        return next((f for f in self.functions if f.identifier == identifier), None)

    def typeByIdentifier(self, identifier):
        return next((t for t in self.types if t.identifier == identifier), None)

    def extensionByIdentifier(self, identifier):
        return next((e for e in self.extensions if e.identifier.endswith(identifier)), None)
    
    def extensionsByCoreVersion(self):
        result = {}
        for version in [ version for version in self.versions if isinstance(version, Version) ]:
            for extension in version.requiredExtensions:
                result[extension] = version
        return result
    
    def extensionsByFunction(self):
        result = {}
        for function in self.functions:
            result[function] = [ extension for extension in function.requiringFeatureSets if isinstance(extension, Extension) and extension in self.extensions ]
        return result

    def printSummary(self):
        print("%s API (%s)" % (self.identifier, self.revision))
        print("")

        print("VENDORS")
        for vendor in self.vendors:
            print("%s (%s)" % (vendor.token, vendor.name))
        print("")

        print("TYPES")
        for type in self.types:
            print(type.identifier + (" ("+type.declaration+")" if hasattr(type, "declaration") else "") \
                + (" => " + type.aliasedType.identifier if hasattr(type, "aliasedType") else ""))
            if hasattr(type, "values"):
                print("[ %s ]" % (", ".join([ value.identifier + "(" + value.value + ")" for value in type.values ])))
        print("")

        print("FUNCTIONS")
        for function in self.functions:
            print(function.returnType.identifier + " " + function.identifier + "(" + ", ".join([ param.type.identifier + " " + param.name for param in function.parameters ]) + ")")
        print("")

        print("VERSIONS")
        for version in self.versions:
            print(version.identifier)
            print("Extensions " + ", ".join([extension.identifier for extension in version.requiredExtensions]))
            print("Functions " + ", ".join([function.identifier for function in version.requiredFunctions]))
            print("Constants " + ", ".join([value.identifier for value in version.requiredConstants]))
            print("Types " + ", ".join([type.identifier for type in version.requiredTypes]))
            print("")
        print("")

        print("EXTENSIONS")
        for extension in self.extensions:
            print(extension.identifier)
            print("Functions " + ", ".join([ function.identifier for function in extension.requiredFunctions ]))
            print("Constants " + ", ".join([ value.identifier for value in extension.requiredConstants]))
            print("Types " + ", ".join([type.identifier for type in extension.requiredTypes]))
            print("")
        print("")
