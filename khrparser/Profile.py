
import os.path

class Profile:
    
    def __init__(self, jsonObject, targetDir):
        self.targetDir = targetDir
        
        self.parserIdentifier = jsonObject["parser"]
        self.generatorIdentifier = jsonObject["generator"]

        self.lowercasePrefix = jsonObject["lowercasePrefix"]
        self.uppercasePrefix = jsonObject["uppercasePrefix"]

        self.api = jsonObject["baseNamespace"]
        self.baseNamespace = jsonObject["baseNamespace"]
        self.inputfilepath = jsonObject["sourceFile"]
        self.inputfile = os.path.basename(self.inputfilepath)
        self.apiIdentifier = jsonObject["apiIdentifier"]
        self.multiContextBinding = jsonObject["multiContext"]
        self.booleanWidth = jsonObject["booleanWidth"]
        self.bindingNamespace = jsonObject["bindingNamespace"]
        self.minCoreVersion = jsonObject["coreProfileSince"]
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
        self.undefs = jsonObject["undefs"] if "undefs" in jsonObject else []
