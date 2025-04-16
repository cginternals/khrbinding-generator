
import re

from khrparser.XMLParser import XMLParser

from khrapi.Version import Version
from khrapi.FeatureSet import FeatureSet
from khrapi.Extension import Extension

from khrapi.Import import Import
from khrapi.TypeAlias import TypeAlias
from khrapi.NativeType import NativeType

from khrapi.Vendor import Vendor
from khrapi.Enumerator import Enumerator
from khrapi.BitfieldGroup import BitfieldGroup
from khrapi.ValueGroup import ValueGroup
from khrapi.SpecialValues import SpecialValues
from khrapi.Constant import Constant
from khrapi.Function import Function
from khrapi.Parameter import Parameter
from khrapi.NativeCode import NativeCode
from khrapi.CompoundType import CompoundType

class ANParser(XMLParser):

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

        # Add Bitfield Type
        bitfieldType = BitfieldGroup(api, profile.bitfieldType)
        unusedBitConstant = Constant(api, "AN_UNUSED_BIT", "0x00000000")
        unusedBitConstant.decimalValue = 0
        bitfieldType.values.append(unusedBitConstant)
        unusedBitConstant.groups.append(bitfieldType)
        api.types.append(bitfieldType)
        api.constants.append(unusedBitConstant)

        # Add requires for basic types
        firstVersion = api.versions[0] # hopefully 1.0

        firstVersion.requiredTypes.append(api.typeByIdentifier(profile.bitfieldType))
        firstVersion.requiredTypes.append(api.typeByIdentifier("AnError"))

        # Fix requires for constants that are defined through enumerators
        for version in api.versions:
            enumerators = [ type for type in version.requiredTypes if isinstance(type, Enumerator) ]
            version.requiredConstants += [ constant for enumerator in enumerators for constant in enumerator.values ]

        return api
    
    @classmethod
    def filterAPI(cls, api, profile):

        return api

    @classmethod
    def deriveBinding(cls, api, profile):

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
        
        # Fix enum type
        fixedEnumType = Enumerator(api, profile.enumType)
        oldEnumType = api.typeByIdentifier(profile.enumType)
        if oldEnumType in api.types:
            api.types.remove(oldEnumType)

        for type in [ type for type in api.types if isinstance(type, Enumerator) ]:
            for value in type.values:
                value.groups.append(fixedEnumType)
                fixedEnumType.values.append(value)
            if not profile.useEnumGroups:
                type.hideDeclaration = True

        api.types.insert(1, fixedEnumType)

        # Add extension type
        extensionType = Enumerator(api, profile.extensionType)
        extensionType.unsigned = False
        api.types.insert(1, extensionType)
        
        # Fix boolean type
        booleanType = Enumerator(api, profile.booleanType)
        booleanType.hideDeclaration = True

        # Remove boolean values from enum
        for constant in api.constants:
            if constant.identifier in [ "AN_TRUE", "AN_FALSE" ]:
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

        # General binding configuration

        binding = super(cls, ANParser).deriveBinding(api, profile)

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
        binding.bitfieldType = profile.bitfieldType
        binding.noneBitfieldValue = profile.noneBitfieldValue
        binding.cStringOutputTypes = profile.cStringOutputTypes
        binding.useEnumGroups = profile.useEnumGroups
        binding.cPointerTypes = [ type.identifier for type in api.types if False ]
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
    def handleNoneType(cls, api, profile, type):

        name = type.attrib["name"] if "name" in type.attrib else type.find("name").text

        nativeType = NativeType(api, name, name)
        nativeType.hideDeclaration = True

        # None-categorized Types likely aren't declared by Anari
        # nativeType.namespacedIdentifier = profile.baseNamespace + "::" + nativeType.identifier

        api.types.append(nativeType)

    @classmethod
    def handleIncludeType(cls, api, profile, type):

        """ Handled Cases:
        * 1. <type name="an_platform" category="include">#include "an_platform.h"</type>
        * 2. <type category="include" name="X11/Xlib.h"/>
        """
        
        name = type.attrib["name"]

        if type.text is not None: # case 1
            importName = re.search('%s(.*)%s' % ('"', '"'), type.text).group(1).strip()
            importType = Import(api, name, "anari/"+importName)
            importType.hideDeclaration = True
            api.dependencies.append(importType)
        else: # case 2
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
    def handleHandleType(cls, api, profile, type):
        """ Handled cases:
        1. <type category="handle">typedef <type>_AnManagedObject</type>* <name>AnObject</name>;</type>
        """

        #if "alias" in type.attrib:
        #    api.types.append(NativeCode(type.attrib["name"], "// Ignore %s for now" % (type.attrib["name"])))
        #    return

        nameTag = type.find("name") # Example: <name>AnObject</name>
        typeTags = type.findall("type") # Example: <type>_AnManagedObject</type>
        
        text = ""
        text += type.text if type.text is not None else "" # Example: typedef

        for typeTag in typeTags:
            text += typeTag.text if typeTag.text else "" # Example: _AnManagedObject
            text += typeTag.tail if typeTag.tail else "" # Example: *
        
        text += nameTag.text if nameTag.text is not None else "" # Example: AnObject
        text += nameTag.tail if nameTag is not None and nameTag.tail else "" # Example: ;

        name = type.attrib["name"] if "name" in type.attrib else nameTag.text

        type = NativeType(api, name, text)
        type.namespacedIdentifier = profile.baseNamespace + "::" + type.identifier
        api.types.append(type)


    @classmethod
    def handleEnumType(cls, api, profile, type):
        
        name = type.attrib["name"] if "name" in type.attrib else None

        enumType = Enumerator(api, name)
        enumType.namespacedIdentifier = profile.baseNamespace + "::" + enumType.identifier
        api.types.append(enumType)


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
        aliasName = aliasName.replace("ANAPI_PTR", "AN_APIENTRY")
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
                    nameTag = member.find("name")
                    memberName = nameTag.text + nameTag.tail if nameTag is not None else ""
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
                pass # currently unused in ANARI
            else:
                structType = CompoundType(api, name, "struct")
                structType.namespacedIdentifier = profile.baseNamespace + "::" + structType.identifier
                api.types.append(structType)

    @classmethod
    def handleUnionType(cls, api, profile, type, parseMembers = False):
        pass # currently unused in ANARI

    @classmethod
    def handleTypeRelations(cls, api, profile, type):
        category = type.attrib.get("category", None)

        if category == "struct":
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
        value = enum.attrib.get("value", None)

        constants = []
        
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
    def detectSpecialValueType(cls, api, enum):
        if not "value" in enum.attrib:
            return None
        
        return cls.obtainNativeType(api, "unsigned int")

    @classmethod
    def obtainNativeType(cls, api, name):
        nativeType = api.typeByIdentifier(name)
        if nativeType is None:
            nativeType = NativeType(api, name, name)
            nativeType.hideDeclaration = True
            api.types.append(nativeType)
        return nativeType

    @classmethod
    def handleFunction(cls, api, profile, command):
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
                    if typeParts[1] in [ "void", "void*", "void**", "int", "float", "int*", "uint32_t*", "size_t*", "uint64_t*", "char*", "char**" ]:
                        pass
                    else:
                        nativeType = typeParts[1].replace('*', '')
                        typeParts[1] = profile.baseNamespace + "::" + typeParts[1]
                else:
                    if typeParts[0] in [ "void", "void*", "void**", "int", "float", "int*", "uint32_t*", "size_t*", "uint64_t*", "char*", "char**" ]:
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
    def handleVersion(cls, api, profile, feature):
        """ Handled cases:
        1. <feature api="anari" name="AN_VERSION_1_0" number="1.0" comment="ANARI core API interface definitions">
        """

        identifier = "an"+"".join([ c for c in feature.attrib["number"] if c.isdigit() ])
        version = Version(api, identifier, feature.attrib["api"], feature.attrib["number"], "an")

        for require in feature.findall("require"):
            cls.handleVersionRequire(api, version, require)

        # For now, ANARI has no deprecated features
        #for remove in feature.findall("remove"):
        #    cls.handleVersionRemove(api, version, remove)
        
        version.supportedAPIs = feature.attrib["api"] # .split("|") # why a split?

        api.versions.append(version)

    @classmethod
    def handleVersionRequire(cls, api, version, require):
        for child in require:
            if child.tag == "enum":
                name = child.attrib["name"]
                constant = api.constantByIdentifier(name)
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
