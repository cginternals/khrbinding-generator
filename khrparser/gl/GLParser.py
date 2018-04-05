
import xml.etree.ElementTree as ET
import re

from khrapi.API import API
from khrapi.Version import Version
from khrapi.Extension import Extension
from khrapi.Import import Import

def inner(xml):
    return str("".join([ t for t in xml.itertext() ]))

class GLParser:
    def parse(profile):
        xmlFile = profile.inputfile
        apiRequire = profile.apiRequire
        
        tree     = ET.parse(xmlFile)
        registry = tree.getroot()
        
        api = API(profile.api)
        
        # Versions
        for feature in registry.iter("feature"):
            if "api" in feature.attrib and feature.attrib["api"] != apiRequire:
                continue
            
            version = Version(api, feature.attrib["name"], feature.attrib["number"])
            
            for require in feature.findall("require"):
                if "api" in require.attrib and require.attrib["api"] != apiRequire:
                    continue
                
                for child in require:
                    if child.tag == "enum":
                        version.requiredConstants.append(api.constantByIdentifier(child.attrib["name"]))
                    elif child.tag == "command":
                        version.requiredFunctions.append(api.functionByIdentifier(child.attrib["name"]))
            
            for remove in feature.findall("remove"):
                if "api" in require.attrib and require.attrib["api"] != apiRequire:
                    continue
                
                for child in remove:
                    if child.tag == "enum":
                        version.removedConstants.append(api.constantByIdentifier(child.attrib["name"]))
                    elif child.tag == "command":
                        version.removedFunctions.append(api.functionByIdentifier(child.attrib["name"]))

            api.versions.append(version)
        
        # Extensions
        for E in registry.iter("extensions"):
            for xmlExtension in E.findall("extension"):
                if "supported" in xmlExtension.attrib and apiRequire not in xmlExtension.attrib["supported"].split("|"):
                    continue

                extension = Extension(api, xmlExtension.attrib["name"])
                    
                for require in xmlExtension.findall("require"):
                    if "api" in require.attrib and require.attrib["api"] != apiRequire:
                        continue
                    
                    for child in require:
                        if child.tag == "enum":
                            extension.requiredConstants.append(api.constantByIdentifier(child.attrib["name"]))
                        elif child.tag == "command":
                            extension.requiredFunctions.append(api.functionByIdentifier(child.attrib["name"]))
                
                api.extensions.append(extension)

        # Types
        for T in registry.iter("types"):
            for type in T.findall("type"):
                if "api" in type.attrib and type.attrib["api"] != apiRequire:
                    continue
                
                nativeDeclaration = inner(type)
                if nativeDeclaration.startswith("#include"):
                    importName = re.search('%s(.*)%s' % ("<", ">"), nativeDeclaration).group(1)
                    api.types.append(Import(api, type.attrib["name"], importName))

        return api
