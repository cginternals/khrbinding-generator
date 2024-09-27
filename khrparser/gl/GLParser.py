
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

import collections.abc

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
                constant.decimalValue = int(enum.attrib["value"], 0)
                if "group" in E.attrib and E.attrib["group"] == "SpecialNumbers":
                    constant.type = cls.detectSpecialValueType(api, enum)
                api.constants.append(constant)

        # Groups
        groups = set([])
        for E in registry.iter("enums"):
            if "group" in E.attrib:
                name = E.attrib["group"]
                groups.update([ name ])
            
            for enum in E.findall("enum"):
                # new feature: <enum> in <enums> may have additional groups, so we have to parse them
                if "group" in enum.attrib:
                    groups.update(enum.attrib["group"].split(","))
            
        for name in groups:
            if name=="VertexShaderWriteMaskEXT":
                # Fix VertexShaderWriteMaskEXT type (is actually a boolean)
                booleanType = api.typeByIdentifier(profile.booleanType)
                if booleanType is None:
                    booleanType = ValueGroup(api, profile.booleanType)
                    booleanType.hideDeclaration = True
                    booleanType.namespacedIdentifier = profile.baseNamespace+"::"+profile.booleanType
                    api.types.append(booleanType)
                type = TypeAlias(api, name, booleanType)
                type.namespacedIdentifier = profile.baseNamespace+"::"+name
            elif name.find("Mask") >= 0 or name == "PathFontStyle":
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
            
            api.types.append(type)
        
        # Register enum values at groups
        for E in registry.iter("enums"):
            name = E.attrib.get("group", None)

            for enum in E.findall("enum"):
                constant = api.constantByIdentifier(enum.attrib["name"])

                if constant is None:
                    continue

                # new feature: <enum> in <enums> may have additional groups, so we have to parse them
                groups = set([ name ] if name is not None else [])
                if "group" in enum.attrib:
                    groups.update(enum.attrib["group"].split(","))
                
                for groupName in groups:
                    group = api.typeByIdentifier(groupName)
                    if group is None:
                        print("Group",groupName,"not found")
                        continue
                    if isinstance(group, TypeAlias):
                        continue
                    
                    # print("Group name", group.identifier)
                    if constant in group.values:
                        continue
                    group.values.append(constant)
                    constant.groups.append(group)

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
                    name = param.find("name").text
                    groupName = param.attrib.get("group", None)
                    groupType = api.typeByIdentifier(groupName)
                    typeTag = param.find("ptype")
                    if groupType is not None and isinstance(groupType, BitfieldGroup):
                        typeName = groupName
                    elif groupType is not None and isinstance(groupType, TypeAlias): # and isinstance(groupType.aliasedType, ValueGroup):
                        typeName = groupName
                    else:
                        typeName = param.text if param.text else ""
                        if typeTag is not None:
                            if typeTag.text:
                                typeName += typeTag.text
                            if typeTag.tail:
                                typeName += typeTag.tail
                        typeName = typeName.strip()
                    type = api.typeByIdentifier(typeName)
                    nativeType = typeName
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
                                nativeType = typeParts[1]
                                typeParts[1] = profile.baseNamespace + "::" + typeParts[1]
                        else:
                            if typeParts[0] == "void":
                                pass
                            else:
                                nativeType = typeParts[0]
                                typeParts[0] = profile.baseNamespace + "::" + typeParts[0]

                        type.namespacedIdentifier = " ".join(typeParts)
                        api.types.append(type)
                    
                    parameter = Parameter(function, name, type)
                    parameter.nativeType = api.typeByIdentifier(nativeType)
                    function.parameters.append(parameter)

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

            version = cls.createVersion(api, feature)
            api.versions.append(version)

        return api

    @classmethod
    def patch(cls, api, profile):

        # Fix Special Values
        specialNumbersType = None
        oldSpecialNumbersType = api.typeByIdentifier("SpecialNumbers")
        if oldSpecialNumbersType is not None:
            api.types.remove(oldSpecialNumbersType)

        for constant in api.constants:
            if "SpecialNumbers" in [ group.identifier for group in constant.groups ] and len(constant.groups) == 1 and constant.type is not None:
                if specialNumbersType is None:
                    specialNumbersType = SpecialValues(api, "SpecialValues")
                    specialNumbersType.hideDeclaration = True
                    api.types.append(specialNumbersType)
            
                specialNumbersType.values.append(constant)
                constant.groups = [specialNumbersType]

        return api
    
    @classmethod
    def filterAPI(cls, api, profile):

        featureSets = []

        mixedAPIs = not isinstance(profile.apiIdentifier, str) and isinstance(profile.apiIdentifier, collections.abc.Sequence)
        if mixedAPIs:
            api.versions = [ version for version in api.versions if any([apiIdentifier in version.supportedAPIs for apiIdentifier in profile.apiIdentifier]) ]
            api.extensions = [ extension for extension in api.extensions if any([apiIdentifier in extension.supportedAPIs for apiIdentifier in profile.apiIdentifier]) ]
        else:
            api.versions = [ version for version in api.versions if profile.apiIdentifier in version.supportedAPIs ]
            api.extensions = [ extension for extension in api.extensions if profile.apiIdentifier in extension.supportedAPIs ]
            
        featureSets += api.versions
        featureSets += api.extensions

        api.constants = [ constant for constant in api.constants if
            any((featureSet for featureSet in featureSets if constant in featureSet.requiredConstants))
        ]
        
        api.functions = [ function for function in api.functions if any((featureSet for featureSet in featureSets if function in featureSet.requiredFunctions)) ]
        
        api.types = [ type for type in api.types if
            any((featureSet for featureSet in featureSets if type in featureSet.requiredTypes)) or
            any((constant for constant in api.constants if type == constant.type or type in constant.groups)) or
            any((function for function in api.functions if type == function.returnType or type in ([ parameter.type for parameter in function.parameters ] + [ parameter.nativeType for parameter in function.parameters ]))) or
            type.identifier in [ "GLuint64", "GLchar", "GLubyte", profile.bitfieldType, "SpecialValues" ]
        ]
        for type in api.types:
            if isinstance(type, BitfieldGroup):
                type.values = [ value for value in type.values if value in api.constants ]
            if isinstance(type, Enumerator):
                type.values = [ value for value in type.values if value in api.constants ]

        api.types = [ type for type in api.types if ((not isinstance(type, BitfieldGroup) and not isinstance(type, Enumerator)) or len(type.values) > 0) ]

        for constant in api.constants:
            constant.groups = [ group for group in constant.groups if group in api.types ]
        
        return api

    @classmethod
    def deriveBinding(cls, api, profile):

        if profile.generateNoneBits:
            # Remove shared enum and bitfield GL_NONE
            noneBit = api.constantByIdentifier("GL_NONE")
            if noneBit is not None:
                for group in noneBit.groups[:]:
                    if isinstance(group, BitfieldGroup):
                        group.values.remove(noneBit)
                        noneBit.groups.remove(group)
                if len(group.values) == 0:
                    api.types.remove(group)
                if len(noneBit.groups) == 0:
                    api.constants.remove(noneBit)

            # Generic None Bit
            genericNoneBit = Constant(api, profile.noneBitfieldValue, "0x0")
            genericNoneBit.decimalValue = 0
            genericNoneBit.generic = True
            api.constants.append(genericNoneBit)
            for group in [ group for group in api.types if isinstance(group, BitfieldGroup)]:
                group.values.append(genericNoneBit)
                genericNoneBit.groups.append(group)

        # Fix GLenum type
        fixedEnumType = Enumerator(api, profile.enumType)
        api.types.remove(api.typeByIdentifier(profile.enumType))

        for type in [ type for type in api.types if isinstance(type, Enumerator) ]:
            for value in type.values:
                value.groups.append(fixedEnumType)
                fixedEnumType.values.append(value)
            if not profile.useEnumGroups:
                type.hideDeclaration = True

        api.types.insert(1, fixedEnumType)
    
        # Fix boolean type
        booleanType = Enumerator(api, profile.booleanType)
        booleanType.hideDeclaration = True

        cls.ensureGLES2Types(api, profile)

        # Remove boolean values from GLenum
        for constant in api.constants:
            if constant.identifier in [ "GL_TRUE", "GL_FALSE" ]:
                for group in constant.groups:
                    group.values.remove(constant)
                constant.groups = [ booleanType ]
                booleanType.values.append(constant)

        # Remove boolean type
        oldBooleanType = next((t for t in api.types if t.identifier == profile.booleanType), None)
        if oldBooleanType is not None:
            api.types.remove(oldBooleanType)
        
        # Finally add boolean type

        api.types.insert(2, booleanType)

        # Assign Ungrouped
        ungroupedType = None
        for constant in api.constants:
            if len(constant.groups) == 0:
                if ungroupedType is None:
                    ungroupedType = Enumerator(api, "UNGROUPED")
                    ungroupedType.hideDeclaration = True
                    api.types.append(ungroupedType)
            
                ungroupedType.values.append(constant)
                constant.groups.append(ungroupedType)
        
        # Add GLextension type
        extensionType = Enumerator(api, profile.extensionType)
        extensionType.unsigned = False
        api.types.insert(0, extensionType)

        # Add unused mask bitfield
        unusedMaskType = BitfieldGroup(api, "UnusedMask")
        unusedBitConstant = Constant(api, "GL_UNUSED_BIT", "0x00000000")
        unusedBitConstant.decimalValue = 0
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
        
        binding = super(cls, GLParser).deriveBinding(api, profile)

        binding.baseNamespace = profile.baseNamespace
        
        binding.multiContextBinding = profile.multiContextBinding
        binding.minCoreVersion = profile.minCoreVersion
        
        binding.identifier = profile.bindingNamespace
        binding.namespace = profile.bindingNamespace
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

        binding.headerGuardMacro = profile.headerGuardMacro
        binding.headerReplacement = profile.headerReplacement

        binding.extensionType = profile.extensionType
        binding.booleanType = profile.booleanType
        binding.booleanWidth = profile.booleanWidth
        binding.enumType = profile.enumType
        binding.bitfieldType = profile.bitfieldType
        binding.noneBitfieldValue = profile.noneBitfieldValue
        binding.cStringOutputTypes = profile.cStringOutputTypes
        binding.useEnumGroups = profile.useEnumGroups
        binding.cPointerTypes = [ type.identifier for type in api.types if type.identifier == "GLvoid" ]
        binding.undefs = profile.undefs

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

    @classmethod
    def createVersion(cls, api, feature_xml):
        internalIdentifier = "".join([c for c in feature_xml.attrib["api"] if not c.isdigit() ] + [ c for c in feature_xml.attrib["number"] if c.isdigit() ])
        version = Version(api, internalIdentifier, feature_xml.attrib["api"], feature_xml.attrib["number"], "".join([c for c in feature_xml.attrib["api"] if not c.isdigit() ]))
        version.supportedAPIs = feature_xml.attrib["api"].split("|")

        for require in feature_xml.findall("require"):
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

        for remove in feature_xml.findall("remove"):
            for child in remove:
                if child.tag == "enum":
                    version.removedConstants.append(api.constantByIdentifier(child.attrib["name"]))
                elif child.tag == "command":
                    version.removedFunctions.append(api.functionByIdentifier(child.attrib["name"]))
                elif child.tag == "type":
                    version.removedTypes.append(api.typeByIdentifier(child.attrib["name"]))

        return version

    @classmethod
    def ensureGLES2Types(cls, api, profile):
        # Add missing types
        if profile.apiIdentifier == "gles2":
            intType = api.typeByIdentifier('int')
            if intType is None:
                intType = NativeType(api, "int", "int")
                intType.hideDeclaration = True
                api.types.append(intType)

            charType = api.typeByIdentifier('char')
            if charType is None:
                charType = NativeType(api, "char", "char")
                charType.hideDeclaration = True
                api.types.append(charType)
                
            voidpType = api.typeByIdentifier('void *')
            if voidpType is None:
                voidpType = NativeType(api, "void *", "void *")
                voidpType.hideDeclaration = True
                api.types.append(voidpType)

            eglIntType = TypeAlias(api, "EGLint", intType)
            eglIntType.namespacedIdentifier = profile.baseNamespace+"::"+eglIntType.identifier
            api.types.append(eglIntType)

            eglCharType = TypeAlias(api, "EGLchar", charType)
            eglCharType.namespacedIdentifier = profile.baseNamespace+"::"+eglCharType.identifier
            api.types.append(eglCharType)

            eglNativeDisplayType = TypeAlias(api, "EGLNativeDisplayType", voidpType)
            eglNativeDisplayType.namespacedIdentifier = profile.baseNamespace+"::"+eglNativeDisplayType.identifier
            api.types.append(eglNativeDisplayType)

            eglNativePixmapType = TypeAlias(api, "EGLNativePixmapType", voidpType)
            eglNativePixmapType.namespacedIdentifier = profile.baseNamespace+"::"+eglNativePixmapType.identifier
            api.types.append(eglNativePixmapType)

            eglNativeWindowType = TypeAlias(api, "EGLNativeWindowType", voidpType)
            eglNativeWindowType.namespacedIdentifier = profile.baseNamespace+"::"+eglNativeWindowType.identifier
            api.types.append(eglNativeWindowType)
