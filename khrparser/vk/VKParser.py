
import xml.etree.ElementTree as ET
import re

from khrapi.API import API
from khrapi.Version import Version
from khrapi.Extension import Extension

from khrapi.Import import Import
from khrapi.TypeAlias import TypeAlias
from khrapi.NativeType import NativeType

from khrapi.Enumerator import Enumerator
from khrapi.BitfieldGroup import BitfieldGroup
from khrapi.Constant import Constant
from khrapi.Function import Function
from khrapi.Parameter import Parameter
from khrapi.NativeCode import NativeCode
from khrapi.CompoundType import CompoundType

class VKParser:
    def parse(profile):
        xmlFile = profile.inputfile
        apiRequire = profile.apiRequire
        
        tree     = ET.parse(xmlFile)
        registry = tree.getroot()
        
        api = API(profile.api, 0)

        # Types
        for T in registry.iter("types"):
            for type in T.findall("type"):
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
                    api.types.append(NativeType(api, name, name))

                elif category == "include":
                    if type.text is not None:
                        importName = re.search('%s(.*)%s' % ('"', '"'), text).group(1).strip()
                        api.types.append(Import(api, name, importName))
                    else:
                        api.types.append(Import(api, name, name))

                elif category == "define":

                    if text.startswith("#define"):
                        api.types.append(NativeCode(name, text))
                    elif text.startswith("typedef"):
                        pass
                    elif text.startswith("struct"):
                        api.types.append(NativeType(api, name, text))
                    else:
                        api.types.append(NativeCode(name, text))

                elif category == "basetype":
                    if text.startswith("typedef") and typeTag is not None:
                        aliasName = typeTag.text
                        alias = api.typeByIdentifier(aliasName)
                        if alias is None:
                            alias = NativeType(api, aliasName, aliasName)

                        api.types.append(TypeAlias(api, name, alias))
                    else:
                        pass

                elif category == "bitmask":
                    if text.startswith("typedef") and typeTag is not None:
                        aliasName = typeTag.text
                        alias = api.typeByIdentifier(aliasName)
                        if alias is None:
                            alias = NativeType(api, aliasName, aliasName)

                        api.types.append(TypeAlias(api, name, alias))
                    else:
                        pass

                elif category == "handle":
                    api.types.append(NativeType(api, name, text))

                elif category == "enum":
                    enumType = Enumerator(api, name)
                    api.types.append(enumType)

                    if "alias" in type.attrib:
                        aliasName = type.attrib["alias"]
                        api.types.append(TypeAlias(api, aliasName, enumType))

                elif category == "funcpointer":
                    aliasName = re.search('%s(.*)%s' % ("typedef ", ";"), text).group(1).strip()
                    alias = api.typeByIdentifier(aliasName)
                    if alias is None:
                        alias = NativeType(api, aliasName, aliasName)

                    api.types.append(TypeAlias(api, name, alias))

                elif category == "struct":
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

                elif category == "union":
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

        # Constants
        for E in registry.iter("enums"):

            nameString = E.attrib.get("name", None)
            typeString = E.attrib.get("type", None)

            if nameString == "API Constants":
                type = Enumerator(api, "UNGROUPED")
                api.types.append(type)
            else:
                type = api.typeByIdentifier(nameString)
                if type is None:
                    if typeString == "enum":
                        type = Enumerator(api, nameString)
                    elif typeString == "bitmask":
                        type = BitfieldGroup(api, nameString)
                    else:
                        type = Enumerator(api, nameString)
                    api.types.append(type)

            for enum in E.findall("enum"):
                name = enum.attrib["name"]
                value = enum.attrib.get("value", None)

                if "bitpos" in enum.attrib:
                    value = str(1 << int(enum.attrib["bitpos"]))

                if value is None:
                    value = name

                constant = Constant(api, name, value)

                if "alias" in enum.attrib:
                    alias = enum.attrib["alias"]
                    aliasConstant = Constant(api, alias, value)
                    constants = [ constant, aliasConstant ]
                else:
                    constants = [ constant ]

                for c in constants:
                    type.values.append(c)
                    c.groups.append(type)
                    api.constants.append(c)

        # Functions
        for C in registry.iter("commands"):
            for command in C.findall("command"):
                if "name" in command.attrib and "alias" in command.attrib:
                    aliasFunction = api.functionByIdentifier(command.attrib["alias"])
                    function = Function(api, command.attrib["name"])
                    function.returnType = aliasFunction.returnType
                    function.parameters = aliasFunction.parameters
                    api.functions.append(function)
                    continue

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

        # Extensions
        for E in registry.iter("extensions"):
            for xmlExtension in E.findall("extension"):
                extension = Extension(api, xmlExtension.attrib["name"])

                for require in xmlExtension.findall("require"):
                    for child in require:
                        if child.tag == "enum":
                            name = child.attrib["name"]
                            constant = api.constantByIdentifier(name)
                            if constant is None:
                                if "extends" in enum.attrib:
                                    type = api.typeByIdentifier(enum.attrib["extends"])
                                else:
                                    type = api.typeByIdentifier("UNGROUPED")

                                if type is None:
                                    type = Enumerator(api, "UNGROUPED")
                                    api.types.append(type)

                                value = enum.attrib.get("value", None)

                                if "bitpos" in enum.attrib:
                                    value = str(1 << int(enum.attrib["bitpos"]))

                                constant = Constant(api, name, value if value else name)

                                if "alias" in enum.attrib:
                                    alias = enum.attrib["alias"]
                                    aliasConstant = Constant(api, alias, value)
                                    constants = [constant, aliasConstant]
                                else:
                                    constants = [constant]

                                for c in constants:
                                    type.values.append(c)
                                    c.groups.append(type)
                                    api.constants.append(c)
                                    extension.requiredConstants.append(c)
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

        # Versions
        for feature in registry.iter("feature"):

            version = Version(api, feature.attrib["name"], feature.attrib["number"])

            for require in feature.findall("require"):
                comment = require.attrib.get("comment", "")
                if comment.startswith("Promoted from "):
                    requiredExtension = re.search('%s([A-Za-z0-9_]+)' % ("Promoted from "), comment).group(1).strip()
                    version.requiredExtensions.append(api.extensionByIdentifier(requiredExtension))

                if comment.startswith("Not used by the API"):
                    continue

                for child in require:
                    if child.tag == "enum":
                        name = child.attrib["name"]
                        constant = api.constantByIdentifier(name)
                        if constant is None:
                            if "extends" in enum.attrib:
                                type = api.typeByIdentifier(enum.attrib["extends"])
                            else:
                                type = api.typeByIdentifier("UNGROUPED")

                            if type is None:
                                type = Enumerator(api, "UNGROUPED")
                                api.types.append(type)

                            value = enum.attrib.get("value", None)

                            if "bitpos" in enum.attrib:
                                value = str(1 << int(enum.attrib["bitpos"]))

                            constant = Constant(api, name, value if value else name)

                            if "alias" in enum.attrib:
                                alias = enum.attrib["alias"]
                                aliasConstant = Constant(api, alias, value)
                                constants = [constant, aliasConstant]
                            else:
                                constants = [constant]

                            for c in constants:
                                type.values.append(c)
                                c.groups.append(type)
                                api.constants.append(c)
                                version.requiredConstants.append(c)
                        else:
                            version.requiredConstants.append(constant)
                    elif child.tag == "command":
                        version.requiredFunctions.append(api.functionByIdentifier(child.attrib["name"]))
                    elif child.tag == "type":
                        requiredType = api.typeByIdentifier(child.attrib["name"])
                        if requiredType is None:
                            requiredType = NativeType(api, child.attrib["name"], child.attrib["name"])
                        version.requiredTypes.append(requiredType)

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

    def patch(self, profile, api):
        return api
