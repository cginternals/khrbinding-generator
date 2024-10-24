
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
from khrapi.SpecialValues import SpecialValues

class VKParser(XMLParser):

    @classmethod
    def parseXML(cls, api, profile, registry):
        deferredFunctionPointerTypes = []
        # Vendors
        for V in registry.iter("tags"):
            for vendor in V.findall("tag"):
                cls.handleVendor(api, profile, vendor)

        # Types
        for T in registry.iter("types"):
            for type in T.findall("type"):
                cls.handleType(api, profile, type, deferredFunctionPointerTypes)
        
        # Create deferred types
        for type in deferredFunctionPointerTypes:
            cls.handleFunctionPointerType(api, profile, type)
        
        # Parse type relations
        for T in registry.iter("types"):
            for type in T.findall("type"):
                cls.handleTypeRelations(api, profile, type)

        # Constants
        for E in registry.iter("enums"):

            type = cls.handleConstantType(api, profile, E)

            for enum in E.findall("enum"):
                cls.handleConstantValue(api, profile, type, enum)

        # Functions
        for C in registry.iter("commands"):
            for command in C.findall("command"):
                cls.handleFunction(api, profile, command)

        # Register Extensions
        for E in registry.iter("extensions"):
            for xmlExtension in E.findall("extension"):
                cls.preHandleExtension(api, profile, xmlExtension)

        # Versions
        # Handle version before extension as some extension alias the values from the core features
        for feature in registry.iter("feature"):
            cls.handleVersion(api, profile, feature)

        # Extensions
        for E in registry.iter("extensions"):
            for xmlExtension in E.findall("extension"):
                cls.handleExtension(api, profile, xmlExtension)

        return api

    @classmethod
    def patch(cls, api, profile):
        return api

    @classmethod
    def filterAPI(cls, api, profile):

        # api.printSummary()

        featureSets = []

        api.versions = [ version for version in api.versions if profile.apiIdentifier in version.supportedAPIs ]
        featureSets += api.versions

        # filter extensions
        api.extensions = [ extension for extension in api.extensions if
            extension.platform == "" and
            not extension.identifier.startswith('RESERVED_DO_NOT_USE') and
            not "_extension_" in extension.identifier and
            profile.apiIdentifier in extension.supportedAPIs
        ]
        featureSets += api.extensions

        api.constants = [ constant for constant in api.constants if
            any((featureSet for featureSet in featureSets if constant in featureSet.requiredConstants))
        ]
        
        for constant in [ constant for constant in api.constants if constant.value == "__TODO_INVALID_VALUE__" ]:
            for group in constant.groups:
                group.values.remove(constant)
            constant.groups = []
            api.constants.remove(constant)

        api.functions = [ function for function in api.functions if any((featureSet for featureSet in featureSets if function in featureSet.requiredFunctions)) ]

        def combine(l1, l2):
            for i in l2:
                if i not in l1 and i is not None:
                    l1.append(i)

        requiredTypes = []
        combine(requiredTypes, [ type for type in api.types if isinstance(type, NativeCode) or type.identifier in [ profile.bitfieldType, "SpecialNumbers", "VkInternalAllocationType", "VkSystemAllocationScope" ] ])
        combine(requiredTypes, [ type for featureSet in featureSets for type in featureSet.requiredTypes ])
        combine(requiredTypes, [ constant.type for constant in api.constants ])
        combine(requiredTypes, [ type for constant in api.constants for type in constant.groups ])
        combine(requiredTypes, [ function.returnType for function in api.functions ])
        combine(requiredTypes, [ parameter.type for function in api.functions for parameter in function.parameters ])
        combine(requiredTypes, [ parameter.nativeType for function in api.functions for parameter in function.parameters ])
        for i in range(1, 10):
            combine(requiredTypes, [ member.type for compoundType in requiredTypes if isinstance(compoundType, CompoundType) for member in compoundType.memberAttributes ])
            combine(requiredTypes, [ member.nativeType for compoundType in requiredTypes if isinstance(compoundType, CompoundType) for member in compoundType.memberAttributes ])
            combine(requiredTypes, [ extensionType for compoundType in requiredTypes if isinstance(compoundType, CompoundType) for extensionType in compoundType.extends ])
            combine(requiredTypes, [ type.aliasedType for type in requiredTypes if isinstance(type, TypeAlias) ])

        api.types = cls.sortTypes(api, requiredTypes)

        # api.types = [ type for type in api.types if ((not isinstance(type, BitfieldGroup) and not isinstance(type, Enumerator)) or len(type.values) > 0) ]
        # api.types = [ type for type in api.types if ((not isinstance(type, TypeAlias) or type.aliasedType in api.types))]

        for constant in api.constants:
            constant.groups = [ group for group in constant.groups if group in api.types ]
        
        for type in api.types:
            if isinstance(type, BitfieldGroup):
                type.values = [ value for value in type.values if value in api.constants ]
            if isinstance(type, Enumerator):
                type.values = [ value for value in type.values if value in api.constants ]
        
        # api.printSummary()

        return api

    @classmethod
    def deriveBinding(cls, api, profile):

        # Remove shared enum and bitfield VK_NONE
        # noneBit = api.constantByIdentifier("VK_NONE")
        # if noneBit is not None:
        #     for group in noneBit.groups[:]:
        #         if isinstance(group, BitfieldGroup):
        #             group.values.remove(noneBit)
        #             noneBit.groups.remove(group)
        #     if len(group.values) == 0:
        #         api.types.remove(group)
        #     if len(noneBit.groups) == 0:
        #         api.constants.remove(noneBit)

        # Fix Special Values
        specialNumbersType = None
        oldSpecialNumbersType = api.typeByIdentifier("SpecialNumbers")
        if oldSpecialNumbersType is not None:
            api.types.remove(oldSpecialNumbersType)

        for constant in api.constants:
            if "SpecialNumbers" in [ group.identifier for group in constant.groups ]:
                if len(constant.groups) == 1 and constant.type is not None:
                    if specialNumbersType is None:
                        specialNumbersType = SpecialValues(api, "SpecialValues")
                        specialNumbersType.hideDeclaration = True
                        api.types.append(specialNumbersType)
                
                    specialNumbersType.values.append(constant)
                    constant.groups = [specialNumbersType]
        
        # Add generic bitfield type
        bitfieldType = api.typeByIdentifier(profile.bitfieldType)
        if bitfieldType is None:
            aliasedType = api.typeByIdentifier("unsigned int")
            if aliasedType is None:
                aliasedType = NativeType(api, "unsigned int", "unsigned int")
                aliasedType.hideDeclaration = True
                api.types.append(aliasedType)
            bitfieldType = TypeAlias(api, profile.bitfieldType, aliasedType)
            bitfieldType.namespacedIdentifier = profile.baseNamespace + "::" + bitfieldType.identifier
            api.types.insert(0, bitfieldType)

        # Generic None Bit
        genericNoneBit = Constant(api, profile.noneBitfieldValue, "0x0")
        genericNoneBit.decimalValue = 0
        genericNoneBit.generic = True
        api.constants.append(genericNoneBit)
        for group in [ group for group in api.types if isinstance(group, BitfieldGroup) ]:
            group.values.append(genericNoneBit)
            genericNoneBit.groups.append(group)

        # Add GLextension type
        extensionType = Enumerator(api, profile.extensionType)
        extensionType.unsigned = False
        api.types.insert(1, extensionType)

        # Fix GLenum type
        oldEnumType = api.typeByIdentifier(profile.enumType)
        if oldEnumType in api.types:
            api.types.remove(oldEnumType)
        api.types.insert(2, Enumerator(api, profile.enumType))

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
        while oldBooleanType is not None: # TODO: check why VkBool32 was in api.types twice
            api.types.remove(oldBooleanType)
            oldBooleanType = next((t for t in api.types if t.identifier == profile.booleanType), None)
        
        # Finally add boolean type

        api.types.insert(3, booleanType)

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
        unusedBitConstant = Constant(api, "VK_UNUSED_BIT", "0x00000000")
        unusedBitConstant.decimalValue = 0
        unusedMaskType.values.append(unusedBitConstant)
        unusedBitConstant.groups.append(unusedMaskType)
        api.types.append(unusedMaskType)
        api.constants.append(unusedBitConstant)

        binding = super(cls, VKParser).deriveBinding(api, profile)

        binding.baseNamespace = profile.baseNamespace
        
        binding.multiContextBinding = profile.multiContextBinding
        
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
        binding.apientry = binding.baseNamespace.upper()+"_APIENTRY"

        binding.headerGuardMacro = profile.headerGuardMacro
        binding.headerReplacement = profile.headerReplacement

        binding.extensionType = profile.extensionType
        binding.booleanType = profile.booleanType
        binding.booleanWidth = profile.booleanWidth
        binding.enumType = profile.enumType
        binding.useEnumGroups = profile.useEnumGroups
        binding.bitfieldType = profile.bitfieldType
        binding.noneBitfieldValue = profile.noneBitfieldValue
        binding.cStringOutputTypes = profile.cStringOutputTypes
        binding.cPointerTypes = [ type.identifier for type in api.types if type.identifier == "CAMetalLayer" ]
        binding.undefs = profile.undefs

        return binding

    @classmethod
    def handleVendor(cls, api, profile, vendor):
        api.vendors.append(
            Vendor(
                vendor.attrib.get("name"),
                vendor.attrib.get("author")
            )
        )

    @classmethod
    def handleType(cls, api, profile, type, deferredFunctionPointerTypes):
        category = type.attrib.get("category", None)

        if category is None:
            cls.handleNoneType(api, profile, type)

        elif category == "include":
            cls.handleIncludeType(api, profile, type)

        elif category == "define":
            cls.handleDefineType(api, profile, type)

        elif category == "basetype":
            cls.handleBaseType(api, profile, type)

        elif category == "enum" and "Bit" in type.attrib["name"]:
            cls.handleBitmaskType(api, profile, type)

        elif category == "bitmask":
            cls.handleBitmask2Type(api, profile, type)

        elif category == "handle":
            cls.handleHandleType(api, profile, type)

        elif category == "enum":
            cls.handleEnumType(api, profile, type)

        elif category == "funcpointer":
            deferredFunctionPointerTypes.append(type)

        elif category == "struct":
            cls.handleStructType(api, profile, type, False)

        elif category == "union":
            cls.handleUnionType(api, profile, type, False)
    
    @classmethod
    def handleTypeRelations(cls, api, profile, type):
        category = type.attrib.get("category", None)

        if "structextends" in type.attrib:
            structType = api.typeByIdentifier(type.attrib["name"])
            typesToMerge = [ api.typeByIdentifier(extension) for extension in type.attrib["structextends"].split(",") ]
            structType.extends = typesToMerge
            memberAttributes = []
            for t in typesToMerge + [ structType ]:
                for member in t.memberAttributes:
                    newMember = next((newMember for newMember in memberAttributes if newMember.name == member.name), None)
                    if newMember is None:
                        parameter = Parameter(structType, member.name, member.type)
                        parameter.nativeType = member.nativeType
                        memberAttributes.append(parameter)
                    else:
                        newMember.type = member.type
                        newMember.nativeType = member.nativeType
            structType.memberAttributes = memberAttributes

        elif category == "struct":
            cls.handleStructType(api, profile, type, True)

        elif category == "union":
            cls.handleUnionType(api, profile, type, True)

    @classmethod
    def handleConstantType(cls, api, profile, E):
        nameString = E.attrib.get("name", None)
        typeString = E.attrib.get("type", None)

        type = api.typeByIdentifier(nameString)
        if type is not None:
            return type

        if nameString == "API Constants":
            type = Enumerator(api, "SpecialNumbers")
            type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
            api.types.append(type)
        else:
            if typeString == "enum":
                type = Enumerator(api, nameString)
            elif typeString == "bitmask":
                type = BitfieldGroup(api, nameString)
            else:
                type = Enumerator(api, nameString)
            type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
            api.types.append(type)
        
        return type

    @classmethod
    def handleConstantValue(cls, api, profile, type, enum):
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
                aliasConstant.decimalValue = int(value, 0)
                constants.append(aliasConstant)
            if aliasConstant.value is not None and value is None:
                value = aliasConstant.value
            constant = Constant(api, name, value if value is not None else name)
            constant.type = aliasConstant.type
        else:
            constant = Constant(api, name, value if value is not None else name)
            constant.type = cls.detectSpecialValueType(api, enum)
        
        constant.decimalValue = 0
        constants.append(constant)

        for c in constants:
            if isinstance(type, TypeAlias):
                type.aliasedType.values.append(c)
                c.groups.append(type)
                c.groups.append(type.aliasedType)
            else:
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
        returnTypeName = (returnTypeTag.text if returnTypeTag is not None else protoTag.text).strip()
        name = protoTag.find("name").text.strip()

        function = Function(api, name)
        returnType = api.typeByIdentifier(returnTypeName)
        if returnType is None:
            returnType = NativeType(api, returnTypeName, returnTypeName)
            returnType.hideDeclaration = True
            returnType.namespacedIdentifier = profile.baseNamespace + "::" + returnType.identifier
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
            name = param.find("name").text.strip()
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
                    if typeParts[1] in [ "void", "void*", "void**", "int", "float", "int*", "uint32_t*", "size_t*", "uint64_t*", "char*" ]:
                        pass
                    else:
                        nativeType = typeParts[1].replace('*', '')
                        typeParts[1] = profile.baseNamespace + "::" + typeParts[1]
                else:
                    if typeParts[0] in [ "void", "void*", "void**", "int", "float", "int*", "uint32_t*", "size_t*", "uint64_t*", "char*" ]:
                        pass
                    else:
                        nativeType = typeParts[0].replace('*', '')
                        typeParts[0] = profile.baseNamespace + "::" + typeParts[0]

                type.namespacedIdentifier = " ".join(typeParts)
                api.types.append(type)

            parameter = Parameter(function, name, type)
            parameter.nativeType = api.typeByIdentifier(nativeType)
            function.parameters.append(parameter)

        api.functions.append(function)

    @classmethod
    def preHandleExtension(cls, api, profile, xmlExtension):
        extension = Extension(api, xmlExtension.attrib["name"], xmlExtension.attrib["platform"] if "platform" in xmlExtension.attrib else "")
        extension.supportedAPIs = xmlExtension.attrib["supported"].split("|")
        api.extensions.append(extension)

    @classmethod
    def handleExtension(cls, api, profile, xmlExtension):
        extension = api.extensionByIdentifier(xmlExtension.attrib["name"])

        for require in xmlExtension.findall("require"):
            for child in require:
                if child.tag == "enum":
                    name = child.attrib["name"]
                    if name.endswith("_NAME"): # Ignore name constants for now
                        continue
                    
                    constant = api.constantByIdentifier(name)
                    if constant is None:
                        if "extends" in child.attrib:
                            type = api.typeByIdentifier(child.attrib["extends"])
                        else:
                            type = api.typeByIdentifier("UNGROUPED")

                        if type is None:
                            type = Enumerator(api, "UNGROUPED")
                            type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
                            api.types.append(type)

                        if "number" in xmlExtension.attrib and "offset" in child.attrib:
                            value = hex(1000000000 + 1000 * (int(xmlExtension.attrib["number"])-1) + int(child.attrib["offset"]))
                        elif "bitpos" in child.attrib:
                            value = hex(1 << int(child.attrib["bitpos"]))
                        elif "alias" in child.attrib:
                            aliasConstant = api.constantByIdentifier(child.attrib["alias"])
                            if aliasConstant is not None:
                                value = aliasConstant.value
                            else:
                                value = child.attrib.get("value", None)
                        else:
                            value = child.attrib.get("value", None)

                        constant = Constant(api, name, value if value is not None else "__TODO_INVALID_VALUE__")
                        try:
                            constant.decimalValue = int(value if value is not None else "0", 0)
                        except:
                            constant.decimalValue = None
                            # TODO: Handle string value

                        if isinstance(type, TypeAlias):
                            type.aliasedType.values.append(constant)
                            constant.groups.append(type.aliasedType)
                        else:
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

    @classmethod
    def handleVersion(cls, api, profile, feature):
        identifier = "vk"+"".join([ c for c in feature.attrib["number"] if c.isdigit() ])
        version = Version(api, identifier, feature.attrib["name"], feature.attrib["number"], "vk")

        for require in feature.findall("require"):
            cls.handleVersionRequire(api, version, require)

        for remove in feature.findall("remove"):
            cls.handleVersionRemove(api, version, remove)
        
        version.supportedAPIs = feature.attrib["api"].split("|")

        api.versions.append(version)

    @classmethod
    def handleVersionRequire(cls, api, version, require):
        comment = require.attrib.get("comment", "")
        if comment.startswith("Promoted from "):
            requiredExtension = re.search('%s([A-Za-z0-9_]+)' % ("Promoted from "), comment).group(1).strip()
            extension = api.extensionByIdentifier(requiredExtension)
            version.requiredExtensions.append(extension)

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
                        type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
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
                    constant.decimalValue = int(value, 0)

                    if isinstance(type, TypeAlias):
                        type.aliasedType.values.append(constant)
                        constant.groups.append(type.aliasedType)
                    else:
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
                    # requiredType = NativeType(api, child.attrib["name"], child.attrib["name"])
                    # version.requiredTypes.append(requiredType)
                    pass
                else:
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
    def handleNoneType(cls, api, profile, type):

        name = type.attrib["name"] if "name" in type.attrib else type.find("name").text

        nativeType = NativeType(api, name, name)
        nativeType.hideDeclaration = True
        # None-categorized Types likely aren't declared by Vulkan
        # nativeType.namespacedIdentifier = profile.baseNamespace + "::" + nativeType.identifier
        api.types.append(nativeType)

    @classmethod
    def handleIncludeType(cls, api, profile, type):

        nameTag = type.find("name")
        typeTags = type.findall("type")
        
        text = ""
        text += type.text if type.text is not None else ""

        for typeTag in typeTags:
            text += typeTag.text if typeTag.text else ""
            text += typeTag.tail if typeTag.tail else ""

        text += nameTag.tail if nameTag is not None and nameTag.tail else ""

        name = type.attrib["name"] if "name" in type.attrib else nameTag.text

        if type.text is not None:
            importName = re.search('%s(.*)%s' % ('"', '"'), text).group(1).strip()
            importType = Import(api, name, "vulkan/"+importName)
            importType.hideDeclaration = True
            api.dependencies.append(importType)
        else:
            importType = Import(api, name, name)
            importType.hideDeclaration = True
            api.dependencies.append(importType)

    @classmethod
    def handleDefineType(cls, api, profile, type):
        nameTag = type.find("name")
        typeTags = type.findall("type")
        
        text = ""
        text += type.text if type.text is not None else ""

        if nameTag is not None:
            text += nameTag.text
            text += nameTag.tail if nameTag.tail is not None else ""

        for typeTag in typeTags:
            text += typeTag.text if typeTag.text is not None else ""
            text += typeTag.tail if typeTag.tail is not None else ""

        definePosition = text.find("#define ")
        structPosition = text.find("struct ")
        typedefPosition = text.find("typedef ")
        if definePosition >= 0 and nameTag is not None:
            api.types.append(NativeCode(nameTag.text, text))
        elif definePosition >= 0 and nameTag is None:
            api.types.append(NativeCode(type.attrib["name"], text))
        elif typedefPosition >= 0:
            api.types.append(NativeCode(nameTag.text, text))
        elif structPosition >= 0:
            type = NativeType(api, nameTag.text, text)
            type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
            api.types.append(type)
        else:
            api.types.append(NativeCode(nameTag.text, text))

    @classmethod
    def handleBaseType(cls, api, profile, type):
        nameTag = type.find("name")
        typeTag = type.find('type')
        if type.text.startswith("typedef") and typeTag is not None and nameTag is not None:
            aliasName = typeTag.text.strip()
            alias = api.typeByIdentifier(aliasName)
            if alias is None:
                alias = NativeType(api, aliasName, aliasName)
                alias.hideDeclaration = True

            type = TypeAlias(api, nameTag.text.strip(), alias)
            type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
            api.types.append(type)
        else:
            pass

    @classmethod
    def handleBitmaskType(cls, api, profile, type):

        nameTag = type.find("name")
        typeTags = type.findall("type")
        
        text = ""
        text += type.text if type.text is not None else ""

        for typeTag in typeTags:
            text += typeTag.text if typeTag.text else ""
            text += typeTag.tail if typeTag.tail else ""

        text += nameTag.tail if nameTag is not None and nameTag.tail else ""

        name = type.attrib["name"] if "name" in type.attrib else nameTag.text

        if api.typeByIdentifier(type.attrib["name"]) is None:
            type = BitfieldGroup(api, type.attrib["name"])
            type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
            api.types.append(type)

    @classmethod
    def handleBitmask2Type(cls, api, profile, type):
        if "name" in type.attrib:
            alias = type.attrib["alias"]
            name = type.attrib["name"]
            bitfieldType = BitfieldGroup(api, name)
            bitfieldType.namespacedIdentifier = profile.baseNamespace + "::" + bitfieldType.identifier
            api.types.append(bitfieldType)
            aliasType = api.typeByIdentifier(alias)
            if aliasType is None:
                aliasType = TypeAlias(api, alias, bitfieldType)
                aliasType.namespacedIdentifier = profile.baseNamespace + "::" + aliasType.identifier
                api.types.append(aliasType)
        else:
            name = type.find("name").text
            if "requires" in type.attrib:
                bitfieldType = BitfieldGroup(api, name)
                bitfieldType.namespacedIdentifier = profile.baseNamespace + "::" + bitfieldType.identifier
                api.types.append(bitfieldType)
                aliasType = api.typeByIdentifier(type.attrib["requires"])
                if aliasType is None:
                    aliasType = TypeAlias(api, type.attrib["requires"], bitfieldType)
                    aliasType.namespacedIdentifier = profile.baseNamespace + "::" + aliasType.identifier
                    api.types.append(aliasType)
            else:
                type = BitfieldGroup(api, name)
                type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
                api.types.append(type)

    @classmethod
    def handleHandleType(cls, api, profile, type):

        if "alias" in type.attrib:
            api.types.append(NativeCode(type.attrib["name"], "// Ignore %s for now" % (type.attrib["name"])))
            return

        nameTag = type.find("name")
        typeTags = type.findall("type")
        
        text = ""
        text += type.text if type.text is not None else ""

        for typeTag in typeTags:
            text += typeTag.text if typeTag.text else ""
            text += typeTag.tail if typeTag.tail else ""

        text += nameTag.tail if nameTag is not None and nameTag.tail else ""

        name = type.attrib["name"] if "name" in type.attrib else nameTag.text

        type = NativeType(api, name, text[0:text.find("(")+1]+name+text[text.find("(")+1:])
        type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
        api.types.append(type)

    @classmethod
    def handleEnumType(cls, api, profile, type):

        nameTag = type.find("name")
        typeTags = type.findall("type")
        
        text = ""
        text += type.text if type.text is not None else ""

        for typeTag in typeTags:
            text += typeTag.text if typeTag.text else ""
            text += typeTag.tail if typeTag.tail else ""

        text += nameTag.tail if nameTag is not None and nameTag.tail else ""

        name = type.attrib["name"] if "name" in type.attrib else nameTag.text

        enumType = Enumerator(api, name)
        enumType.namespacedIdentifier = profile.baseNamespace + "::" + enumType.identifier
        api.types.append(enumType)

        # if "alias" in type.attrib:
        #     aliasName = type.attrib["alias"]
        #     api.types.append(TypeAlias(api, aliasName, enumType))

    @classmethod
    def handleFunctionPointerType(cls, api, profile, type):

        nameTag = type.find("name")
        typeTags = type.findall("type")
        
        text = ""
        text += type.text if type.text is not None else ""

        # text+= nameTag.text
        text += nameTag.tail if nameTag is not None and nameTag.tail else ""

        for typeTag in typeTags:
            text += typeTag.text if typeTag.text else ""
            text += typeTag.tail if typeTag.tail else ""

        name = type.attrib["name"] if "name" in type.attrib else nameTag.text

        text = re.sub(r'\s*\n\s*', '', text)
        aliasName = re.search('%s(.*)%s' % ("typedef ", ";"), text).group(1).strip()
        aliasName = re.sub("\\s+", " ", aliasName)
        aliasName = aliasName.replace("VKAPI_PTR", "VK_APIENTRY")
        alias = api.typeByIdentifier(aliasName)
        if alias is None:
            alias = NativeType(api, aliasName, aliasName)
            alias.hideDeclaration = True
            api.types.append(alias)

        type = TypeAlias(api, name, alias)
        type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
        api.types.append(type)

    @classmethod
    def handleStructType(cls, api, profile, type, parseMembers = False):
        name = type.attrib["name"]

        if parseMembers:
            if "alias" in type.attrib:
                aliasedType = api.typeByIdentifier(type.attrib["alias"])
                structType = TypeAlias(api, name, aliasedType)
                structType.namespacedIdentifier = profile.baseNamespace + "::" + structType.identifier
                api.types.append(structType)
            else:
                structType = api.typeByIdentifier(name)

                for member in type.findall("member"):
                    memberName = member.find("name").text
                    memberTypeTag = member.find("type")
                    memberTypeName = member.text if member.text is not None else ""
                    memberTypeName += memberTypeTag.text
                    memberTypeName += memberTypeTag.tail.strip() if memberTypeTag.tail is not None else ""
                    memberTypeName = memberTypeName.strip()
                    nativeTypeName = memberTypeName

                    memberType = api.typeByIdentifier(memberTypeName)
                    if memberType is None:
                        typeParts = memberTypeName.split(" ")
                        if "struct" in typeParts:
                            typeParts.remove("struct")
                        
                        memberType = NativeType(api, " ".join(typeParts), " ".join(typeParts))
                        memberType.hideDeclaration = True

                        if typeParts[0] == "const":
                            if typeParts[1] in [ "void", "void*", "void**", "int", "float", "int*", "uint32_t*", "size_t*", "uint64_t*", "char*" ]:
                                pass
                            else:
                                nativeTypeName = typeParts[1].replace('*', '')
                                typeParts[1] = profile.baseNamespace + "::" + typeParts[1]
                        else:
                            if typeParts[0] in [ "void", "void*", "void**", "int", "float", "int*", "uint32_t*", "size_t*", "uint64_t*", "char*" ]:
                                pass
                            else:
                                nativeTypeName = typeParts[0].replace('*', '')
                                typeParts[0] = profile.baseNamespace + "::" + typeParts[0]

                        memberType.namespacedIdentifier = " ".join(typeParts)
                        api.types.append(memberType)
                    
                    parameter = Parameter(structType, memberName, memberType)
                    nativeType = api.typeByIdentifier(nativeTypeName)
                    if nativeType is None:
                        nativeType = NativeType(api, nativeTypeName, nativeTypeName)
                        nativeType.hideDeclaration = True
                        api.types.append(nativeType)

                    parameter.nativeType = nativeType
                    structType.memberAttributes.append(parameter)
        else:
            if "alias" in type.attrib:
                pass # do later
            else:
                structType = CompoundType(api, name, "struct")
                structType.namespacedIdentifier = profile.baseNamespace + "::" + structType.identifier
                api.types.append(structType)


    @classmethod
    def handleUnionType(cls, api, profile, type, parseMembers = False):
        name = type.attrib["name"]

        if parseMembers:
            structType = api.typeByIdentifier(name)

            for member in type.findall("member"):
                memberName = member.find("name").text
                memberTypeTag = member.find("type")
                memberTypeName = member.text if member.text is not None else ""
                memberTypeName += memberTypeTag.text
                memberTypeName += memberTypeTag.tail.strip() if memberTypeTag.tail is not None else ""
                memberTypeName = memberTypeName.strip()
                nativeTypeName = memberTypeName

                if nativeTypeName.startswith("const "):
                    nativeTypeName = nativeTypeName[len("const "):].strip()
                while nativeTypeName.endswith("*"):
                    nativeTypeName = nativeTypeName[0:-len("*")].strip()

                memberType = api.typeByIdentifier(memberTypeName)
                if memberType is None:
                    memberType = NativeType(api, memberTypeName, memberTypeName)
                    memberType.hideDeclaration = True
                    api.types.append(memberType)

                parameter = Parameter(structType, memberName, memberType)
                nativeType = api.typeByIdentifier(nativeTypeName)
                if nativeType is None:
                    nativeType = NativeType(api, nativeTypeName, nativeTypeName)
                    nativeType.hideDeclaration = True
                    api.types.append(nativeType)

                parameter.nativeType = nativeType
                structType.memberAttributes.append(parameter)
        else:
            structType = CompoundType(api, name, "union")
            structType.namespacedIdentifier = profile.baseNamespace + "::" + structType.identifier
            api.types.append(structType)

    @classmethod
    def sortTypes(cls, api, types):
        nativeCodes = []
        nativeTypes = []
        enumerators = []
        functionPointerTypes = []
        bitfieldGroups = []
        compoundTypes = []
        aliases = []
        for t in types:
            typesToAdd = [ t ]
            if isinstance(t, NativeCode):
                nativeCodes.append(t)
            elif isinstance(t, NativeType):
                nativeTypes.append(t)
            elif isinstance(t, Enumerator):
                enumerators.append(t)
            elif isinstance(t, BitfieldGroup):
                bitfieldGroups.append(t)
            elif isinstance(t, CompoundType):
                compoundTypes.append(t)
            elif isinstance(t, TypeAlias):
                if t.identifier.startswith('PFN'):
                    functionPointerTypes.append(t)
                else:
                    aliases.append(t)
            else:
                pass
        
        def collect(topologySortedCompoundTypes, compoundType):
            for type in [ member.type for member in compoundType.memberAttributes ] + [ member.nativeType for member in compoundType.memberAttributes ]:
                if isinstance(type, CompoundType) and not type == compoundType and not type in topologySortedCompoundTypes:
                    collect(topologySortedCompoundTypes, type)
    
            if not compoundType in topologySortedCompoundTypes:
                topologySortedCompoundTypes.append(compoundType)
            else:
                pass
                # print("Cyclic dependency of", compoundType.identifier,"?")
        
        # sort nativeCodes
        # pass

        # sort nativeTypes
        nativeTypes.sort(key=lambda t: t.identifier)

        # sort enumerators
        enumerators.sort(key=lambda t: t.identifier)

        # sort bitfieldGroups
        bitfieldGroups.sort(key=lambda t: t.identifier)

        # sort functionPointerTypes
        functionPointerTypes.sort(key=lambda t: t.identifier)

        # sort compoundTypes
        topologySortedCompoundTypes = []
        for compoundType in compoundTypes:
            collect(topologySortedCompoundTypes, compoundType)

        # unaliasedTypes
        unaliasedTypes = [ alias for alias in aliases if alias.aliasedType.hideDeclaration or alias.aliasedType not in types ]

        types = []
        for t in (nativeCodes + nativeTypes + enumerators + bitfieldGroups + functionPointerTypes + unaliasedTypes + topologySortedCompoundTypes):
            alias = next((a for a in aliases if a.aliasedType == t), None)
            types.append(t)
            if alias is not None:
                types.append(alias)

        return types

    @classmethod
    def detectSpecialValueType(cls, api, enum):
        if not "value" in enum.attrib:
            return None
        
        if "." in enum.attrib["value"] and enum.attrib["value"].endswith("f"):
            return cls.obtainNativeType(api, "float")
        elif "ULL" in enum.attrib["value"]:
            return cls.obtainNativeType(api, "unsigned long long")
        elif "U" in enum.attrib["value"]:
            return cls.obtainNativeType(api, "unsigned int")

        return cls.obtainNativeType(api, "unsigned int")

    @classmethod
    def obtainNativeType(cls, api, name):
        nativeType = api.typeByIdentifier(name)
        if nativeType is None:
            nativeType = NativeType(api, name, name)
            nativeType.hideDeclaration = True
            api.types.append(nativeType)
        return nativeType
