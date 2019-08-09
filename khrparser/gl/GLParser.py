
import re

from khrparser.XMLParser import XMLParser

from khrapi.Version import Version
from khrapi.FeatureSet import FeatureSet
from khrapi.Extension import Extension

from khrapi.Import import Import
from khrapi.TypeAlias import TypeAlias
from khrapi.NativeType import NativeType

from khrapi.Enumerator import Enumerator
from khrapi.BitfieldGroup import BitfieldGroup
from khrapi.ValueGroup import ValueGroup
from khrapi.SpecialValues import SpecialValues
from khrapi.Constant import Constant
from khrapi.Function import Function
from khrapi.Parameter import Parameter

class GLParser(XMLParser):

    @classmethod
    def parseXML(cls, api, profile, registry):
        # Types
        for T in registry.iter("types"):
            for type in T.findall("type"):
                apiEntryTag = type.find("apientry")
                nameTag = type.find("name")
                text = type.text
                if apiEntryTag is not None and apiEntryTag.tail is not None:
                    if text is None:
                        text = "{{binding.apientry}} " + apiEntryTag.tail.strip()
                    else:
                        text = text + "{{binding.apientry}} " + apiEntryTag.tail.strip()

                if nameTag is not None and nameTag.tail is not None:
                    if text is None:
                        text = nameTag.tail.strip()
                    else:
                        text = text + nameTag.tail.strip()

                if type.tail is not None:
                    if text is None:
                        text = type.tail.strip()
                    else:
                        text = text + type.tail.strip()

                if text is None:
                    text = type.find("name").text

                if nameTag is not None and nameTag.text.startswith("struct"):
                    name = re.search('%s(.*)%s' % ("struct ", ""), nameTag.text).group(1).strip()
                    newType = NativeType(api, name, nameTag.text + text)
                    newType.namespacedIdentifier = profile.baseNamespace+"::"+name
                    api.types.append(newType)

                elif text.startswith("#include"):
                    importName = re.search('%s(.*)%s' % ("<", ">"), text).group(1).strip()
                    api.dependencies.append(Import(api, type.attrib["name"], importName))

                elif text.startswith("#if"):
                    newType = NativeType(api, type.attrib["name"], text)
                    newType.namespacedIdentifier = profile.baseNamespace+"::"+type.attrib["name"]
                    api.types.append(newType)

                elif text.startswith("typedef"):
                    aliasName = re.search('%s(.*)%s' % ("typedef ", ";"), text).group(1).strip()
                    alias = api.typeByIdentifier(aliasName)
                    if alias is None:
                        alias = NativeType(api, aliasName, aliasName)

                    typename = nameTag.text
                    newType = TypeAlias(api, typename, alias)
                    newType.namespacedIdentifier = profile.baseNamespace+"::"+typename
                    api.types.append(newType)

        # Constants
        for E in registry.iter("enums"):
            for enum in E.findall("enum"):
                if api.constantByIdentifier(enum.attrib["name"]) is not None:
                    continue
                
                constant = Constant(api, enum.attrib["name"], enum.attrib["value"])
                if "group" in E.attrib and E.attrib["group"] == "SpecialNumbers":
                    constant.type = cls.detectSpecialValueType(api, enum)
                api.constants.append(constant)

        # Groups

        for G in registry.iter("groups"):
            for group in G.findall("group"):
                name = group.attrib["name"]

                if name.find("Mask") >= 0 or name == "PathFontStyle":
                    type = BitfieldGroup(api, name)
                    type.namespacedIdentifier = profile.baseNamespace+"::"+name
                elif name.find("Boolean") >= 0:
                    type = ValueGroup(api, name)
                    type.hideDeclaration = True
                    type.namespacedIdentifier = profile.baseNamespace+"::"+name
                else:
                    type = Enumerator(api, name)
                    type.hideDeclaration = True
                    type.namespacedIdentifier = profile.baseNamespace+"::"+name
                
                for enum in group.findall("enum"):
                    constant = api.constantByIdentifier(enum.attrib["name"])
                    if constant is None or constant in type.values:
                        continue
                    type.values.append(constant)
                    constant.groups.append(type)
                
                if len(type.values) > 0:
                    api.types.append(type)
        
        for E in registry.iter("enums"):
            if "group" in E.attrib:
                name = E.attrib["group"]

                type = api.typeByIdentifier(name)

                if type is None and (name.find("Mask") >= 0 or name == "PathFontStyle"):
                    type = BitfieldGroup(api, name)
                    type.namespacedIdentifier = profile.baseNamespace+"::"+name
                    api.types.append(type)
                elif type is None and name.find("Boolean") >= 0:
                    type = ValueGroup(api, name)
                    type.hideDeclaration = True
                    type.namespacedIdentifier = profile.baseNamespace+"::"+name
                    api.types.append(type)
                elif type is None:
                    type = Enumerator(api, name)
                    type.hideDeclaration = True
                    type.namespacedIdentifier = profile.baseNamespace+"::"+name
                    api.types.append(type)

                for enum in E.findall("enum"):
                    constant = api.constantByIdentifier(enum.attrib["name"])
                    if constant is None or constant in type.values:
                        continue
                    type.values.append(constant)
                    constant.groups.append(type)

        # Functions
        for C in registry.iter("commands"):
            for command in C.iter("command"):
                protoTag = command.find("proto")
                returnTypeTag = protoTag.find("ptype")
                returnTypeName = " ".join([ text.strip() for text in [ protoTag.text if protoTag is not None else "", returnTypeTag.text if returnTypeTag is not None else "", returnTypeTag.tail if returnTypeTag is not None else "" ] if text is not None ]).strip()
                name = protoTag.find("name").text.strip()

                function = Function(api, name)
                function.namespaceLessIdentifier = function.identifier[len(profile.lowercasePrefix):]
                returnType = api.typeByIdentifier(returnTypeName)
                if returnType is None:
                    returnType = NativeType(api, returnTypeName, returnTypeName)
                    returnType.hideDeclaration = True
                    api.types.append(returnType)
                function.returnType = returnType

                for param in command.findall("param"):
                    groupName = param.attrib.get("group", None)
                    groupType = api.typeByIdentifier(groupName)
                    typeTag = param.find("ptype")
                    if groupType is not None and isinstance(groupType, BitfieldGroup):
                        typeName = groupName
                    else:
                        typeName = param.text if param.text else ""
                        if typeTag is not None:
                            if typeTag.text:
                                typeName += typeTag.text
                            if typeTag.tail:
                                typeName += typeTag.tail
                        typeName = typeName.strip()
                    name = param.find("name").text
                    type = api.typeByIdentifier(typeName)
                    if type is None:
                        typeParts = typeName.split(" ")
                        if "struct" in typeParts:
                            typeParts.remove("struct")
                        
                        type = NativeType(api, " ".join(typeParts), " ".join(typeParts))
                        type.hideDeclaration = True

                        if typeParts[0] == "const":
                            if typeParts[1] == "void":
                                pass
                            else:
                                typeParts[1] = profile.baseNamespace + "::" + typeParts[1]
                        else:
                            if typeParts[0] == "void":
                                pass
                            else:
                                typeParts[0] = profile.baseNamespace + "::" + typeParts[0]

                        type.namespacedIdentifier = " ".join(typeParts)
                        api.types.append(type)

                    function.parameters.append(Parameter(function, name, type))

                api.functions.append(function)

        # Extensions
        for E in registry.iter("extensions"):
            for xmlExtension in E.findall("extension"):
                extension = Extension(api, xmlExtension.attrib["name"])
                extension.supportedAPIs = xmlExtension.attrib["supported"].split("|")

                for require in xmlExtension.findall("require"):
                    for child in require:
                        if child.tag == "enum":
                            extension.requiredConstants.append(api.constantByIdentifier(child.attrib["name"]))
                        elif child.tag == "command":
                            function = api.functionByIdentifier(child.attrib["name"])
                            extension.requiredFunctions.append(function)
                            function.requiringFeatureSets.append(extension)
                        elif child.tag == "type":
                            extension.requiredTypes.append(api.typeByIdentifier(child.attrib["name"]))

                api.extensions.append(extension)

        # Versions
        for feature in registry.iter("feature"):

            version = Version(api, feature.attrib["api"], feature.attrib["number"])
            version.supportedAPIs = feature.attrib["api"].split("|")

            for require in feature.findall("require"):
                comment = require.attrib.get("comment", "")
                if comment.startswith("Reuse tokens from "):
                    requiredExtension = re.search('%s([A-Za-z0-9_]+)' % ("Reuse tokens from "), comment).group(1).strip()
                    version.requiredExtensions.append(api.extensionByIdentifier(requiredExtension))
                elif comment.startswith("Reuse commands from "):
                    requiredExtension = re.search('%s([A-Za-z0-9_]+)' % ("Reuse commands from "), comment).group(1).strip()
                    version.requiredExtensions.append(api.extensionByIdentifier(requiredExtension))
                elif comment.startswith("Reuse "):
                    requiredExtension = re.search('%s([A-Za-z0-9_]+)' % ("Reuse "), comment).group(1).strip()
                    version.requiredExtensions.append(api.extensionByIdentifier(requiredExtension))
                elif comment.startswith("Promoted from "):
                    requiredExtension = re.search('%s([A-Za-z0-9_]+)' % ("Promoted from "), comment).group(1).strip()
                    version.requiredExtensions.append(api.extensionByIdentifier(requiredExtension))

                if comment.startswith("Not used by the API"):
                    continue

                for child in require:
                    if child.tag == "enum":
                        version.requiredConstants.append(api.constantByIdentifier(child.attrib["name"]))
                    elif child.tag == "command":
                        function = api.functionByIdentifier(child.attrib["name"])
                        version.requiredFunctions.append(function)
                        function.requiringFeatureSets.append(version)
                    elif child.tag == "type":
                        version.requiredTypes.append(api.typeByIdentifier(child.attrib["name"]))

            for remove in feature.findall("remove"):
                for child in remove:
                    if child.tag == "enum":
                        version.removedConstants.append(api.constantByIdentifier(child.attrib["name"]))
                    elif child.tag == "command":
                        version.removedFunctions.append(api.functionByIdentifier(child.attrib["name"]))
                    elif child.tag == "type":
                        version.removedTypes.append(api.typeByIdentifier(child.attrib["name"]))

            api.versions.append(version)

        return api

    @classmethod
    def patch(cls, profile, api):

        # Add GLextension type
        extensionType = Enumerator(api, profile.extensionType)
        extensionType.unsigned = False
        api.types.insert(0, extensionType)

        # Fix GLenum type
        api.types.remove(api.typeByIdentifier(profile.enumType))
        api.types.insert(1, Enumerator(api, profile.enumType))

        # Fix boolean type
        booleanType = Enumerator(api, profile.booleanType)
        booleanType.hideDeclaration = True

        # Remove boolean values from GLenum
        for constant in api.constants:
            for group in [ group for group in constant.groups if group.identifier == profile.enumType ]:
                group.values.remove(constant)
                constant.groups.remove(group)
            if constant.identifier in [ "GL_TRUE", "GL_FALSE" ]:
                for group in constant.groups:
                    group.values.remove(constant)
                constant.groups = [ booleanType ]
                booleanType.values.append(constant)

        # Remove boolean type
        oldBooleanType = next((t for t in api.types if isinstance(t, TypeAlias) and t.identifier == profile.booleanType), None)
        api.types.remove(oldBooleanType)
        
        # Finally add boolean type

        api.types.insert(2, booleanType)

        # Generic None Bit
        genericNoneBit = Constant(api, profile.noneBitfieldValue, "0x0")
        genericNoneBit.generic = True
        api.constants.append(genericNoneBit)
        for group in [ group for group in api.types if isinstance(group, BitfieldGroup) ]:
            group.values.append(genericNoneBit)
            genericNoneBit.groups.append(group)

        # Remove shared enum and bitfield GL_NONE
        noneBit = api.constantByIdentifier("GL_NONE")
        if noneBit is not None:
            for group in noneBit.groups:
                if isinstance(group, BitfieldGroup):
                    group.values.remove(noneBit)
            if len(noneBit.groups) == 0:
                api.constants.remove(noneBit)

        # Fix Special Values
        specialNumbersType = None
        api.types.remove(api.typeByIdentifier("SpecialNumbers"))
        for constant in api.constants:
            if len(constant.groups) == 1 and constant.groups[0].identifier == "SpecialNumbers" and constant.type is not None:
                if specialNumbersType is None:
                    specialNumbersType = SpecialValues(api, "SpecialValues")
                    specialNumbersType.hideDeclaration = True
                    api.types.append(specialNumbersType)
            
                specialNumbersType.values.append(constant)
                constant.groups = [specialNumbersType]

        # Assign Ungrouped
        ungroupedType = None
        for constant in api.constants:
            if len(constant.groups) == 0 and constant.type is None:
                if ungroupedType is None:
                    ungroupedType = Enumerator(api, "UNGROUPED")
                    ungroupedType.hideDeclaration = True
                    api.types.append(ungroupedType)
            
                ungroupedType.values.append(constant)
                constant.groups.append(ungroupedType)
        
        # Add unused mask bitfield
        unusedMaskType = BitfieldGroup(api, "UnusedMask")
        unusedBitConstant = Constant(api, "GL_UNUSED_BIT", "0x00000000")
        unusedMaskType.values.append(unusedBitConstant)
        unusedBitConstant.groups.append(unusedMaskType)
        api.types.append(unusedMaskType)
        api.constants.append(unusedBitConstant)

        # Add static cast to negative Enum values
        for constant in api.constants:
            if constant.value.startswith("-") and len(constant.groups) > 0:
                if isinstance(constant.groups[0], Enumerator):
                    constant.value = "static_cast<std::underlying_type<%s>::type>(%s)" % (profile.enumType, constant.value)
                else:
                    constant.value = "static_cast<std::underlying_type<%s>::type>(%s)" % (constant.groups[0].identifier, constant.value)
        
        return api
    
    @classmethod
    def filterAPI(cls, api, profile):

        featureSets = []

        api.versions = [ version for version in api.versions if profile.apiIdentifier in version.supportedAPIs ]
        featureSets += api.versions

        api.extensions = [ extension for extension in api.extensions if profile.apiIdentifier in extension.supportedAPIs ]
        featureSets += api.extensions

        api.constants = [ constant for constant in api.constants if any((featureSet for featureSet in featureSets if constant in featureSet.requiredConstants)) ]
        api.functions = [ function for function in api.functions if any((featureSet for featureSet in featureSets if function in featureSet.requiredFunctions)) ]
        # api.types = api.types

        return api

    @classmethod
    def deriveBinding(cls, api, profile):
        binding = super(cls, GLParser).deriveBinding(api, profile)

        binding.baseNamespace = profile.baseNamespace
        
        binding.multiContextBinding = profile.multiContextBinding
        binding.minCoreVersion = profile.minCoreVersion
        
        binding.identifier = api.identifier+"binding"
        binding.namespace = api.identifier+"binding"
        binding.auxIdentifier = "aux"
        binding.auxNamespace = "aux"
        binding.bindingAuxIdentifier = binding.identifier + "-" + binding.auxIdentifier
        binding.bindingAuxNamespace = binding.namespace + "::" + binding.auxNamespace
        binding.apiExport = binding.identifier.upper() + "_API"
        binding.apiTemplateExport = binding.identifier.upper() + "_TEMPLATE_API"
        binding.auxApiExport = binding.identifier.upper() + "_" + binding.auxIdentifier.upper() + "_API"
        binding.auxApiTemplateExport = binding.identifier.upper() + "_" + binding.auxIdentifier.upper() + "_TEMPLATE_API"
        binding.constexpr = binding.identifier.upper() + "_CONSTEXPR"
        binding.threadlocal = binding.identifier.upper() + "_THREAD_LOCAL"
        binding.useboostthread = binding.identifier.upper() + "_USE_BOOST_THREAD"
        binding.apientry = api.identifier.upper()+"_APIENTRY"

        binding.additionalTypes = ""
        
        binding.headerGuardMacro = profile.headerGuardMacro
        binding.headerReplacement = profile.headerReplacement

        binding.extensionType = profile.extensionType
        binding.booleanType = profile.booleanType
        binding.booleanWidth = profile.booleanWidth
        binding.enumType = profile.enumType
        binding.bitfieldType = profile.bitfieldType
        binding.noneBitfieldValue = profile.noneBitfieldValue

        return binding

    @classmethod
    def detectSpecialValueType(cls, api, enum):
        if "comment" in enum.attrib:
            if re.search('Not an API enum.*', enum.attrib["comment"]) is not None:
                return None

            result = re.search('%s([A-Za-z0-9_]+)' % ("Tagged as "), enum.attrib["comment"])
            if result is not None:
                typeName = result.group(1).strip()
                return next((t for t in api.types if t.identifier.endswith(typeName)), api.typeByIdentifier("GLuint"))
        
        return api.typeByIdentifier("GLuint")
