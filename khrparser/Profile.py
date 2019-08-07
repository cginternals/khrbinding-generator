
import os.path

class Profile:
    
    def __init__(self, jsonObject, targetDir):
        self.targetDir = targetDir
        
        self.parserIdentifier = jsonObject["parser"]
        self.generatorIdentifier = jsonObject["generator"]

        self.api = jsonObject["baseNamespace"]
        self.baseNamespace = jsonObject["baseNamespace"]
        self.inputfilepath = jsonObject["sourceFile"]
        self.inputfile = os.path.basename(self.inputfilepath)
        self.patchfile = jsonObject["patchFile"]
        self.apiRequire = jsonObject["apiIdentifier"]
        self.multiContextBinding = jsonObject["multiContext"]
        self.booleanWidth = jsonObject["booleanWidth"]
        self.bindingNamespace = jsonObject["bindingNamespace"]
        self.minCoreVersion = [ int(number) for number in jsonObject["coreProfileSince"].split(".") ] if jsonObject["coreProfileSince"] else False
        self.extensionType = jsonObject["extensionType"]
        self.noneBitfieldValue = jsonObject["noneBitfieldValue"]
        self.enumType = jsonObject["enumType"]
        self.bitfieldType = jsonObject["bitfieldType"]
        self.booleanType = jsonObject["booleanType"]
