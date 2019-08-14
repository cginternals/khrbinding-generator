
import re

from khrparser.XMLParser import XMLParser

from khrapi.Version import Version
from khrapi.Extension import Extension

from khrapi.Import import Import
from khrapi.TypeAlias import TypeAlias
from khrapi.NativeType import NativeType

from khrapi.Vendor import Vendor
from khrapi.Enumerator import Enumerator
from khrapi.BitfieldGroup import BitfieldGroup
from khrapi.Constant import Constant
from khrapi.Function import Function
from khrapi.Parameter import Parameter
from khrapi.NativeCode import NativeCode
from khrapi.CompoundType import CompoundType

class VKParser(XMLParser):

    @classmethod
    def parseXML(cls, api, profile, registry):
        # Vendors
        for V in registry.iter("tags"):
            for vendor in V.findall("tag"):
                cls.handleVendor(api, vendor)

        # Types
        for T in registry.iter("types"):
            for type in T.findall("type"):
                cls.handleType(api, type)

        # Constants
        for E in registry.iter("enums"):

            type = cls.handleConstantType(api, E)

            for enum in E.findall("enum"):
                cls.handleConstantValue(api, type, enum)

        # Functions
        for C in registry.iter("commands"):
            for command in C.findall("command"):
                cls.handleFunction(api, profile, command)

        # Versions
        for feature in registry.iter("feature"):
            cls.handleVersion(api, feature)

        # Extensions
        for E in registry.iter("extensions"):
            for xmlExtension in E.findall("extension"):
                cls.handleExtension(api, xmlExtension)

        return api

    @classmethod
    def patch(cls, api, profile):
        return api

    @classmethod
    def filterAPI(cls, api, profile):

        # filter extensions
        api.extensions = [ extension for extension in api.extensions if not extension.identifier.startswith('RESERVED_DO_NOT_USE') ]
        api.extensions = [ extension for extension in api.extensions if not "_extension_" in extension.identifier ]

        for constant in [ constant for constant in api.constants if constant.value == "__TODO_INVALID_VALUE__" ]:
            for group in constant.groups:
                group.values.remove(constant)
            constant.groups = []
            api.constants.remove(constant)

        return api

    @classmethod
    def deriveBinding(cls, api, profile):

        # Remove shared enum and bitfield VK_NONE
        noneBit = api.constantByIdentifier("VK_NONE")
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
        genericNoneBit.generic = True
        api.constants.append(genericNoneBit)
        for group in [ group for group in api.types if isinstance(group, BitfieldGroup) ]:
            group.values.append(genericNoneBit)
            genericNoneBit.groups.append(group)

        # Add GLextension type
        extensionType = Enumerator(api, profile.extensionType)
        extensionType.unsigned = False
        api.types.insert(0, extensionType)

        # Fix GLenum type
        oldEnumType = api.typeByIdentifier(profile.enumType)
        if oldEnumType in api.types:
            api.types.remove(oldEnumType)
        api.types.insert(1, Enumerator(api, profile.enumType))

        # Fix boolean type
        booleanType = Enumerator(api, profile.booleanType)
        booleanType.hideDeclaration = True

        # Remove boolean values from GLenum
        for constant in api.constants:
            if constant.identifier in [ "VK_TRUE", "VK_FALSE" ]:
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
        
        # Add unused mask bitfield
        unusedMaskType = BitfieldGroup(api, "UnusedMask")
        unusedBitConstant = Constant(api, "GL_UNUSED_BIT", "0x00000000")
        unusedMaskType.values.append(unusedBitConstant)
        unusedBitConstant.groups.append(unusedMaskType)
        api.types.append(unusedMaskType)
        api.constants.append(unusedBitConstant)

        binding = super(cls, VKParser).deriveBinding(api, profile)

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

        return binding

    @classmethod
    def handleVendor(cls, api, vendor):
        api.vendors.append(
            Vendor(
                vendor.attrib.get("name"),
                vendor.attrib.get("author")
            )
        )

    @classmethod
    def handleType(cls, api, type):
        nameTag = type.find("name")
        typeTags = type.findall("type")
        category = type.attrib.get("category", None)

        text = ""
        text += type.text if type.text else ""
        text += nameTag.tail if nameTag is not None and nameTag.tail else ""

        for typeTag in typeTags:
            text += typeTag.text if typeTag.text else ""
            text += typeTag.tail if typeTag.tail else ""

        text = re.sub(r'\s*\n\s*', '', text)

        name = type.attrib["name"] if "name" in type.attrib else nameTag.text

        if category is None:
            cls.handleNoneType(api, type, name, text)

        elif category == "include":
            cls.handleIncludeType(api, type, name, text)

        elif category == "define":
            cls.handleDefineType(api, type, name, text)

        elif category == "basetype":
            cls.handleBaseType(api, type, name, text)

        elif category == "enum" and "Bit" in type.attrib["name"]:
            cls.handleBitmaskType(api, type, name, text)

        elif category == "handle":
            cls.handleHandleType(api, type, name, text)

        elif category == "enum":
            cls.handleEnumType(api, type, name, text)

        elif category == "funcpointer":
            cls.handleFunctionPointerType(api, type, name, text)

        elif category == "struct":
            cls.handleStructType(api, type, name, text)

        elif category == "union":
            cls.handleUnionType(api, type, name, text)

    @classmethod
    def handleConstantType(cls, api, E):
        nameString = E.attrib.get("name", None)
        typeString = E.attrib.get("type", None)

        type = api.typeByIdentifier(nameString)
        if type is not None:
            return type

        if nameString == "API Constants":
            type = Enumerator(api, "UNGROUPED")
            api.types.append(type)
        else:
            if typeString == "enum":
                type = Enumerator(api, nameString)
            elif typeString == "bitmask":
                type = BitfieldGroup(api, nameString)
            else:
                type = Enumerator(api, nameString)
            api.types.append(type)
        
        return type

    @classmethod
    def handleConstantValue(cls, api, type, enum):
        name = enum.attrib["name"]
        if "extnumber" in enum.attrib and "offset" in enum.attrib:
            value = hex(1000000000 + 1000 * (int(enum.attrib["extnumber"])-1) + int(enum.attrib["offset"]))
        elif "bitpos" in enum.attrib:
            value = hex(1 << int(enum.attrib["bitpos"]))
        else:
            value = enum.attrib.get("value", None)

        constants = []
        if "alias" in enum.attrib:
            aliasConstant = api.constantByIdentifier(enum.attrib["alias"])
            if aliasConstant is None:
                aliasConstant = Constant(api, alias, value)
                constants.append(aliasConstant)
            if aliasConstant.value is not None and value is None:
                value = aliasConstant.value
        
        constant = Constant(api, name, value if value is not None else name)
        constants.append(constant)

        for c in constants:
            type.values.append(c)
            c.groups.append(type)
            api.constants.append(c)

    @classmethod
    def handleFunction(cls, api, profile, command):
        if "name" in command.attrib and "alias" in command.attrib:
            aliasFunction = api.functionByIdentifier(command.attrib["alias"])
            function = Function(api, command.attrib["name"])
            function.returnType = aliasFunction.returnType
            function.parameters = aliasFunction.parameters
            function.namespaceLessIdentifier = function.identifier[len(profile.lowercasePrefix):]
            api.functions.append(function)
            return

        protoTag = command.find("proto")
        returnTypeTag = protoTag.find("type")
        returnTypeName = returnTypeTag.text.strip() if returnTypeTag is not None else protoTag.text.strip()
        name = protoTag.find("name").text.strip()

        function = Function(api, name)
        returnType = api.typeByIdentifier(returnTypeName)
        if returnType is None:
            returnType = NativeType(api, returnTypeName, returnTypeName)
            api.types.append(returnType)
        function.returnType = returnType
        function.namespaceLessIdentifier = function.identifier[len(profile.lowercasePrefix):]

        for param in command.findall("param"):
            groupName = None # param.attrib.get("group", None) # Ignore group names for now
            typeTag = param.find("type")
            if groupName is not None:
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
                type = NativeType(api, typeName, typeName)
                api.types.append(type)

            function.parameters.append(Parameter(function, name, type))

        api.functions.append(function)

    @classmethod
    def handleExtension(cls, api, xmlExtension):
        extension = Extension(api, xmlExtension.attrib["name"])

        for require in xmlExtension.findall("require"):
            for child in require:
                if child.tag == "enum":
                    name = child.attrib["name"]
                    constant = api.constantByIdentifier(name)
                    if constant is None:
                        if "extends" in child.attrib:
                            type = api.typeByIdentifier(child.attrib["extends"])
                        else:
                            type = api.typeByIdentifier("UNGROUPED")

                        if type is None:
                            type = Enumerator(api, "UNGROUPED")
                            api.types.append(type)

                        if "number" in xmlExtension.attrib and "offset" in child.attrib:
                            value = hex(1000000000 + 1000 * (int(xmlExtension.attrib["number"])-1) + int(child.attrib["offset"]))
                        elif "bitpos" in child.attrib:
                            value = hex(1 << int(child.attrib["bitpos"]))
                        else:
                            value = child.attrib.get("value", None)

                        if "alias" in child.attrib:
                            alias = child.attrib["alias"]
                            aliasConstant = api.constantByIdentifier(alias)
                            if aliasConstant is not None:
                                value = aliasConstant.value

                        constant = Constant(api, name, value if value else name)

                        type.values.append(constant)
                        constant.groups.append(type)
                        api.constants.append(constant)
                        extension.requiredConstants.append(constant)
                    else:
                        extension.requiredConstants.append(constant)
                elif child.tag == "command":
                    extension.requiredFunctions.append(api.functionByIdentifier(child.attrib["name"]))
                elif child.tag == "type":
                    requiredType = api.typeByIdentifier(child.attrib["name"])
                    if requiredType is None:
                        requiredType = NativeType(api, child.attrib["name"], child.attrib["name"])
                    extension.requiredTypes.append(requiredType)

        api.extensions.append(extension)

    @classmethod
    def handleVersion(cls, api, feature):
        identifier = "vk"+"".join([ c for c in feature.attrib["number"] if c.isdigit() ])
        version = Version(api, identifier, feature.attrib["name"], feature.attrib["number"], "vk")

        for require in feature.findall("require"):
            cls.handleVersionRequire(api, version, require)

        for remove in feature.findall("remove"):
            cls.handleVersionRemove(api, version, remove)

        api.versions.append(version)

    @classmethod
    def handleVersionRequire(cls, api, version, require):
        comment = require.attrib.get("comment", "")
        if comment.startswith("Promoted from "):
            requiredExtension = re.search('%s([A-Za-z0-9_]+)' % ("Promoted from "), comment).group(1).strip()
            version.requiredExtensions.append(api.extensionByIdentifier(requiredExtension))

        if comment.startswith("Not used by the API"):
            return

        for child in require:
            if child.tag == "enum":
                name = child.attrib["name"]
                constant = api.constantByIdentifier(name)
                if constant is None:
                    if "extends" in child.attrib:
                        type = api.typeByIdentifier(child.attrib["extends"])
                    else:
                        type = api.typeByIdentifier("UNGROUPED")

                    if type is None:
                        type = Enumerator(api, "UNGROUPED")
                        api.types.append(type)

                    if "extnumber" in child.attrib and "offset" in child.attrib:
                        value = hex(1000000000 + 1000 * (int(child.attrib["extnumber"])-1) + int(child.attrib["offset"]))
                    elif "bitpos" in child.attrib:
                        value = hex(1 << int(child.attrib["bitpos"]))
                    else:
                        value = child.attrib.get("value", None)

                    if "alias" in child.attrib:
                        alias = child.attrib["alias"]
                        aliasConstant = api.constantByIdentifier(alias)
                        if aliasConstant is not None:
                            value = aliasConstant.value
                    
                    constant = Constant(api, name, value if value else name)

                    type.values.append(constant)
                    constant.groups.append(type)
                    api.constants.append(constant)
                    version.requiredConstants.append(constant)
                else:
                    version.requiredConstants.append(constant)
            elif child.tag == "command":
                version.requiredFunctions.append(api.functionByIdentifier(child.attrib["name"]))
            elif child.tag == "type":
                requiredType = api.typeByIdentifier(child.attrib["name"])
                if requiredType is None:
                    requiredType = NativeType(api, child.attrib["name"], child.attrib["name"])
                version.requiredTypes.append(requiredType)

    @classmethod
    def handleVersionRemove(cls, api, version, remove):
        for child in remove:
            if child.tag == "enum":
                version.removedConstants.append(api.constantByIdentifier(child.attrib["name"]))
            elif child.tag == "command":
                version.removedFunctions.append(api.functionByIdentifier(child.attrib["name"]))
            elif child.tag == "type":
                version.removedTypes.append(api.typeByIdentifier(child.attrib["name"]))

    @classmethod
    def handleNoneType(cls, api, type, name, text):
        api.types.append(NativeType(api, name, name))

    @classmethod
    def handleIncludeType(cls, api, type, name, text):
        if type.text is not None:
            importName = re.search('%s(.*)%s' % ('"', '"'), text).group(1).strip()
            api.dependencies.append(Import(api, name, importName))
        else:
            api.dependencies.append(Import(api, name, name))

    @classmethod
    def handleDefineType(cls, api, type, name, text):
        if text.startswith("#define"):
            api.types.append(NativeCode(name, text))
        elif text.startswith("typedef"):
            pass
        elif text.startswith("struct"):
            api.types.append(NativeType(api, name, text))
        else:
            api.types.append(NativeCode(name, text))

    @classmethod
    def handleBaseType(cls, api, type, name, text):
        typeTag = type.find('type')
        if text.startswith("typedef") and typeTag is not None:
            aliasName = typeTag.text
            alias = api.typeByIdentifier(aliasName)
            if alias is None:
                alias = NativeType(api, aliasName, aliasName)

            api.types.append(TypeAlias(api, name, alias))
        else:
            pass

    @classmethod
    def handleBitmaskType(cls, api, type, name, text):
        api.types.append(BitfieldGroup(api, type.attrib["name"]))

    @classmethod
    def handleHandleType(cls, api, type, name, text):
        api.types.append(NativeType(api, name, text))

    @classmethod
    def handleEnumType(cls, api, type, name, text):
        enumType = Enumerator(api, name)
        api.types.append(enumType)

        if "alias" in type.attrib:
            aliasName = type.attrib["alias"]
            api.types.append(TypeAlias(api, aliasName, enumType))

    @classmethod
    def handleFunctionPointerType(cls, api, type, name, text):
        aliasName = re.search('%s(.*)%s' % ("typedef ", ";"), text).group(1).strip()
        alias = api.typeByIdentifier(aliasName)
        if alias is None:
            alias = NativeType(api, aliasName, aliasName)

        api.types.append(TypeAlias(api, name, alias))

    @classmethod
    def handleStructType(cls, api, type, name, text):
        structType = CompoundType(api, name, "struct")
        for member in type.findall("member"):
            memberName = member.find("name").text
            memberTypeTag = member.find("type")

            memberTypeName = ""
            memberTypeName += member.text if member.text else ""
            memberTypeName += memberTypeTag.text if memberTypeTag.text else ""
            memberTypeName += memberTypeTag.tail if memberTypeTag.tail else ""

            memberType = api.typeByIdentifier(memberTypeName)
            if memberType is None:
                memberType = NativeType(api, memberTypeName, memberTypeName)
                api.types.append(memberType)
            structType.memberAttributes.append(Parameter(structType, memberName, memberType))

    @classmethod
    def handleUnionType(cls, api, type, name, text):
        structType = CompoundType(api, name, "union")
        for member in type.findall("member"):
            memberName = member.find("name").text
            memberTypeTag = member.find("type")

            memberTypeName = ""
            memberTypeName += member.text if member.text else ""
            memberTypeName += memberTypeTag.text if memberTypeTag.text else ""
            memberTypeName += memberTypeTag.tail if memberTypeTag.tail else ""

            memberType = api.typeByIdentifier(memberTypeName)
            if memberType is None:
                memberType = NativeType(api, memberTypeName, memberTypeName)
                api.types.append(memberType)
            structType.memberAttributes.append(Parameter(structType, memberName, memberType))
