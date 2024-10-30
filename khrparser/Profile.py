
import os.path

class Profile:
    
    def __init__(self, jsonObject, targetDir):
        self.targetDir = targetDir
        
        self.parserIdentifier = jsonObject["parser"]
        self.generatorIdentifier = jsonObject["generator"]

        self.lowercasePrefix = jsonObject["lowercasePrefix"]
        self.uppercasePrefix = jsonObject["uppercasePrefix"]
        self.baseNamespace = jsonObject["baseNamespace"]
        self.inputfilepath = jsonObject["sourceFile"]
        self.inputfile = os.path.basename(self.inputfilepath)
        self.multiContextBinding = jsonObject["multiContext"]
        self.booleanWidth = jsonObject["booleanWidth"]
        self.bindingNamespace = jsonObject["bindingNamespace"]
        self.extensionType = jsonObject["extensionType"]
        self.noneBitfieldValue = jsonObject["noneBitfieldValue"]
        self.useEnumGroups = jsonObject["useEnumGroups"]
        self.enumType = jsonObject["enumType"]
        self.bitfieldType = jsonObject["bitfieldType"]
        self.booleanType = jsonObject["booleanType"]
        self.headerGuardMacro = jsonObject["headerGuardMacro"]
        self.headerReplacement = jsonObject["headerReplacement"]
        self.cStringOutputTypes = jsonObject["cStringOutputTypes"]
        self.generateNoneBits = jsonObject["generateNoneBits"]
        self.stripFeatureHeaders = jsonObject["stripFeatureHeaders"] if "stripFeatureHeaders" in jsonObject else False
        self.undefs = jsonObject["undefs"] if "undefs" in jsonObject else []

        if "apis" in jsonObject and isinstance(jsonObject["apis"], list):
            self.apis = { api["identifier"]: { "entryPointHeader": api["entryPointHeader"] } for api in jsonObject["apis"] }
            for api in jsonObject["apis"]:
                if "coreProfileSince" in api:
                    self.apis[api["identifier"]]["coreProfileSince"] = api["coreProfileSince"]

        # Compatibility with old profile JSON format:
        elif jsonObject["apiIdentifier"]:
            self.apis = { jsonObject["apiIdentifier"]: { "entryPointHeader": self.baseNamespace } }
            if jsonObject["coreProfileSince"]:
                self.apis[jsonObject["apiIdentifier"]]["coreProfileSince"] = jsonObject["coreProfileSince"]
                
