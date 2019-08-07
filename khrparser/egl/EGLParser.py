
import re

from khrparser.XMLParser import XMLParser

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

class EGLParser(XMLParser):

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
                        text = apiEntryTag.tail.strip()
                    else:
                        text = text + apiEntryTag.tail.strip()

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
                    declaration = type.find("name").text

                    if declaration.startswith("struct"):
                        name = re.search('%s(.*)%s' % ("struct ", ""), declaration).group(1).strip()
                        api.types.append(NativeType(api, name, declaration))

                elif text.startswith("#include"):
                    importName = re.search('%s(.*)%s' % ("<", ">"), text).group(1).strip()
                    api.types.append(Import(api, type.attrib["name"], importName))

                elif text.startswith("#if"):
                    api.types.append(NativeType(api, type.attrib["name"], text))

                elif text.startswith("typedef"):
                    aliasName = re.search('%s(.*)%s' % ("typedef ", ";"), text).group(1).strip()
                    alias = api.typeByIdentifier(aliasName)
                    if alias is None:
                        alias = NativeType(api, aliasName, aliasName)

                    typename = nameTag.text
                    api.types.append(TypeAlias(api, typename, alias))

        # Enumerators
        constantNamesByGroupName = dict()
        groupNamesByConstantName = dict()
        for G in registry.iter("groups"):

            for group in G.findall("group"):
                name = group.attrib["name"]

                if name.endswith("Mask"):
                    type = BitfieldGroup(api, name)
                else:
                    type = Enumerator(api, name)

                api.types.append(type)

                for enum in group.findall("enum"):
                    enumName = enum.attrib["name"]
                    if not name in constantNamesByGroupName:
                        constantNamesByGroupName[name] = [ enumName ]
                    else:
                        constantNamesByGroupName[name].append(enumName)
                    if not enumName in groupNamesByConstantName:
                        groupNamesByConstantName[enumName] = [ name ]
                    else:
                        groupNamesByConstantName[enumName].append(name)

        # Constants
        for E in registry.iter("enums"):

            groupString = E.attrib.get("group", None)
            groupType = E.attrib.get("type", None)
            groupNamespace = E.attrib.get("namespace", None)

            if groupString:
                type = Enumerator(api, groupString)
                api.types.append(type)
            elif groupNamespace == "EGL":
                type = api.typeByIdentifier("UNGROUPED")
                if not type:
                    type = Enumerator(api, "UNGROUPED")
                    api.types.append(type)
            elif groupNamespace.endswith("Mask"):
                type = BitfieldGroup(api, groupNamespace)
                api.types.append(type)


            for enum in E.findall("enum"):
                name = enum.attrib["name"]

                constant = Constant(api, name, enum.attrib["value"])

                groupNames = groupNamesByConstantName[name] if name in groupNamesByConstantName else []

                type.values.append(constant)
                constant.groups.append(type)

                api.constants.append(constant)

        # Functions
        for C in registry.iter("commands"):
            for command in C.iter("command"):
                protoTag = command.find("proto")
                returnTypeTag = protoTag.find("ptype")
                if returnTypeTag:
                    print(returnTypeTag.text)
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
                    typeTag = param.find("ptype")
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
                            extension.requiredConstants.append(api.constantByIdentifier(child.attrib["name"]))
                        elif child.tag == "command":
                            extension.requiredFunctions.append(api.functionByIdentifier(child.attrib["name"]))
                        elif child.tag == "type":
                            extension.requiredTypes.append(api.typeByIdentifier(child.attrib["name"]))

                api.extensions.append(extension)

        # Versions
        for feature in registry.iter("feature"):

            version = Version(api, feature.attrib["name"], feature.attrib["number"])

            for require in feature.findall("require"):
                comment = require.attrib.get("comment", None)
                if comment:
                    requiredExtension = re.search('([A-Za-z0-9_]+)', comment).group(1).strip()
                    version.requiredExtensions.append(api.extensionByIdentifier(requiredExtension))

                for child in require:
                    if child.tag == "enum":
                        version.requiredConstants.append(api.constantByIdentifier(child.attrib["name"]))
                    elif child.tag == "command":
                        version.requiredFunctions.append(api.functionByIdentifier(child.attrib["name"]))
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

    @classmethod
    def patch(cls, profile, api):
        return api

    @classmethod
    def deriveBinding(cls, api, profile, binding):
        return binding
    