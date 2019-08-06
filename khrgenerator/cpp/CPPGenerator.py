
import os, sys
from os.path import join as pjoin
import time
import re
import pystache

execDir = os.path.dirname(os.path.abspath(sys.argv[0])) + "/"
templateDir = "templates/"
templateExtension = "tpl"
tab = "    "
tab2 = tab + tab


class Extension:

	suffixes = [   \
		"AMD",     \
		"APPLE",   \
		"ARB",     \
		"ATI",     \
		"EXT",     \
		"GREMEDY", \
		"IBM",     \
		"IMG",     \
		"INGR",    \
		"INTEL",   \
		"KHR",     \
		"NV",      \
		"OES",     \
		"OML",     \
		"PGI",     \
		"QCOM",    \
		"SGIS",    \
		"SGIX",    \
		"VIV",     \
		"WEBGL",   \
		"WIN"]


def versionBID(feature, core=False, ext=False):
    if feature is None:
        return ""

    version = str(feature.major) + str(feature.minor)

    if core:
        return version + "core"
    elif ext:
        return version + "ext"

    return version


def template(outputfile):
    with open(execDir + templateDir + outputfile + ".in", "rU") as file:
        return file.read()


def supportedLambda(obj):
    return lambda feature, core, ext: (not ext and obj.supported(feature, core)
                                       or ext and not obj.supported(feature, False))


def enumSuffixPriority(name):
    index = name.rfind("_")
    if index < 0:
        return -1

    ext = name[index + 1:]

    if ext not in Extension.suffixes:
        return -1

    return Extension.suffixes.index(ext)


def genBitfieldContexts(enums, bitfGroups):
    bitfieldEnums = [enum for enum in enums if enum.type == "GLbitfield"]
    eglBitfieldEnums = [enum for enum in enums if enum.type == "EGLbitfield"]

    if len(bitfieldEnums) == 0 and len(eglBitfieldEnums) == 0:
        return []

    noneIdentifier = "GL_NONE_BIT"
    if len(eglBitfieldEnums) > 0:
        noneIdentifier = "EGL_NONE_BIT"
        bitfieldEnums = eglBitfieldEnums

    maxLength = max([len(enumBID(enum)) for enum in bitfieldEnums])

    noneValue = "0x0"
    noneGroups = Context.listContext([g.name for g in bitfGroups], sortKey=lambda g: g)

    bitfieldContexts = []
    bitfieldContexts.append({"identifier": noneIdentifier,
                             "name": noneIdentifier,
                             "value": noneValue,
                             "spaces": " " * (maxLength - len(noneIdentifier)),
                             "generic": True,
                             "groups": noneGroups,
                             "primaryGroup": noneGroups["items"][0]["item"] if not noneGroups["empty"] else None,
                             "supported": (lambda feature, core, ext: True)})
    for enum in bitfieldEnums:
        groups = Context.listContext([g.name for g in enum.groups], sortKey=lambda g: g)
        bitfieldContexts.append({"identifier": enumBID(enum),
                                 "name": enum.name,
                                 "value": enum.value,
                                 "spaces": " " * (maxLength - len(enumBID(enum))),
                                 "generic": False,
                                 "groups": groups,
                                 "primaryGroup": groups["items"][0]["item"] if not groups["empty"] else None,
                                 "supported": supportedLambda(enum)})
    return bitfieldContexts


def genBooleanContexts(enums):
    booleanEnums = [enum for enum in enums if enum.type == "GLboolean" or enum.type == "EGLBoolean"]
    booleanContexts = []
    for enum in booleanEnums:
        booleanContexts.append({"identifier": enumBID(enum),
                                "name": enum.name,
                                "value": enum.value})
    return booleanContexts


def genEnumContexts(allEnums):
    ungroupedName = "__UNGROUPED__"
    enums = [enum for enum in allEnums if enum.type == "GLenum" or enum.type == "EGLenum"]

    if len(enums) == 0:
        return []

    maxLength = max([len(enumBID(enum)) for enum in enums])
    enumContexts = []
    for enum in enums:
        groups = Context.listContext([g.name for g in enum.groups] if enum.groups else [ungroupedName],
                                     sortKey=lambda g: g)
        enumContexts.append({"identifier": enumBID(enum),
                             "name": enum.name,
                             "value": enum.value,
                             "type": enum.type,
                             "decimalValue": int(enum.value, 0) if enum.value.startswith("0x") else "",
                             "cast": enum.value.startswith("-"),
                             "spaces": " " * (maxLength - len(enumBID(enum))),
                             "groups": groups,
                             "primaryGroup": groups["items"][0]["item"] if not groups["empty"] else None,
                             "supported": supportedLambda(enum)})
    return enumContexts


def genFeatureContexts(features):

    featureContexts = []
    for feature in sorted(features) :

        commandContexts = Context.listContext([{"identifier": c } for c in feature.reqCommandStrings],
            sortKey = lambda c: c["identifier"])

        featureContexts.append({
            "identifier": versionBID(feature),
            "major": feature.major,
            "minor": feature.minor,
            "reqCommandStrings": commandContexts})

    return featureContexts


def typeContext(typeString, namespace=None):
    #TODO-LW reliably split typeString into its logical components
    noNamespace = " void" in typeString or typeString.startswith("void")
    noNamespace = noNamespace or (" int" in typeString or typeString.startswith("int"))
    noNamespace = noNamespace or (" char" in typeString or typeString.startswith("char"))
    hasModifier = typeString.startswith("const ")
    modifier = typeString[0:5] if hasModifier else None
    if hasModifier:
        typeString = typeString[6:]
    typeString = typeString[7:] if typeString.startswith("struct ") else typeString
    return {"modifiers": modifier,
            "ns": None if noNamespace else namespace,
            "type": typeString}

def genFunctionContexts(commands):
    contexts = []
    for command in commands:
        paramContexts = []
        for param in command.params:
            paramContexts.append(
               {"name": param.name,
                "type": typeContext(param.groupString
                                    if (param.type == "GLbitfield" or param.type == "EGLbitfield") and param.groupString
                                    else param.type, command.api) })

        identifier = functionBID(command)
        contexts.append({"identifier": identifier,
                         "identifierNoGl": identifier[2:] if identifier.startswith("gl") else (identifier[3:] if identifier.startswith("egl") else identifier),
                         "type": typeContext(command.returntype, command.api),
                         "params": Context.listContext(paramContexts),
                         "supported": supportedLambda(command) })

    return contexts


def genExtensionContexts(extensions):
    extensionContexts = []
    for extension in extensions:
        commandContexts = Context.listContext([{"identifier": functionBID(c), "name": c.name} for c in extension.reqCommands],
                                              sortKey = lambda c: c["identifier"])
        extensionContexts.append({"identifier": extensionBID(extension),
                                  "name": extension.name,
                                  "incore": extension.incore,
                                  "incoreMajor": extension.incore.major if extension.incore else None,
                                  "incoreMinor": extension.incore.minor if extension.incore else None,
                                  "reqCommands": commandContexts})
    return extensionContexts


REGULAR_TYPE_INTEGRATIONS = {
    "GLextension" : [ "hashable", "streamable", "valueRepresentable" ],
    "EGLextension" : [ "hashable", "streamable", "valueRepresentable" ],
    "GLboolean"   : [ "streamable", "valueRepresentable" ],
    "EGLbBolean"   : [ "streamable", "valueRepresentable" ],
    "GLenum"      : [ "hashable", "streamable", "addable", "comparable", "valueRepresentable" ],
    "EGLenum"      : [ "hashable", "streamable", "addable", "comparable", "valueRepresentable" ],
    "GLbitfield": [],
    "EGLbitfield": [],
    "GLvoid"      : [],
    "EGLvoid"      : [],
    "_cl_context": [],
    "_cl_event": []
}
BITFIELD_TYPE_INTEGRATIONS = [ "hashable", "bitfieldStreamable", "bitOperatable", "valueRepresentable" ]
TYPE_INTEGRATIONS = [ "addable", "bitOperatable", "bitfieldStreamable", "comparable", "hashable", "streamable", "valueRepresentable" ]


def integrationMap(integrationList):
    return { integration: (integration in integrationList) for integration in TYPE_INTEGRATIONS}


def typeIntegrationMap(type):
    return integrationMap(REGULAR_TYPE_INTEGRATIONS[type.name] if type.name in REGULAR_TYPE_INTEGRATIONS else ["valueRepresentable"])


# ToDo: move this to Type class? (as well as convert an multiline convert)
enum_classes = [ "GLenum", "EGLenum" ]

def convertTypedefLine(line, name):

    if not line.startswith("typedef"):
        return line
    else:
        return "using " + name + " = " + line[8:].replace(name, "")


def multilineConvertTypedef(type):

    return "\n".join([ convertTypedefLine(line, type.name) for line in type.value.split('\n') ])


def convertTypedef(type):

    if '\n' in type.value:
        return multilineConvertTypedef(type)

    t = parseType(type)

    if type.name in enum_classes:
        return "enum class " + type.name + " : " + t + ";"

    if not type.value.startswith("typedef"):
        return t
    elif type.name == "GLboolean":
        return "// Import of GLboolean is an include"
    elif type.name == "EGLBoolean":
        return "// Import of EGLBoolean is an include"
    else:
        return "using " + type.name + " = " + t + ";"


def convertType(type, api):

    return convertTypedef(type).replace(" ;", ";").replace("( *)", "(*)").replace("(*)", "("+api.upper()+"_APIENTRY *)")


def genTypeContexts(types, bitfGroups, api):
    extensionTypeName = ("EGL" if api == "egl" else "GL")+"extension"
    typeContexts = [{"identifier": extensionTypeName,
                     "definition": "enum class "+extensionTypeName+" : int;",
                     "integrations": integrationMap([ "hashable", "streamable", "valueRepresentable" ]),
                     "hasIntegrations": True,
                     "isStruct": False}]
    if api == "egl":
        typeContexts.append({"identifier": "EGLbitfield",
                             "definition": "enum class EGLbitfield : unsigned int;",
                             "integrations": integrationMap([]),
                             "hasIntegrations": False,
                             "isStruct": False })
    for type in types: #TODO-LW: explicitly sort types and bitfGroups
        if type.name == "GLuint_array_2" and api=="egl":
            continue
        integrations = typeIntegrationMap(type)
        typeContexts.append({"identifier": type.name,
                             "definition": convertType(type, api),
                             "integrations": integrations,
                             "hasIntegrations": any(integrations.values()),
                             "isStruct": type.typevalue == "struct" })
    for bitf in bitfGroups:
        integrations = integrationMap(BITFIELD_TYPE_INTEGRATIONS)
        typeContexts.append({"identifier": bitf.name,
                             "definition": "enum class {} : unsigned int;".format(bitf.name),
                             "integrations": integrations,
                             "hasIntegrations": any(integrations.values()),
                             "isStruct": type.typevalue == "struct" })
    return typeContexts


def genValueContexts(enums):
    typeBlacklist = ["GLboolean", "GLenum", "GLbitfield", "EGLBoolean", "EGLenum", "EGLbitfield"]
    valueEnums = [enum for enum in enums if enum.type not in typeBlacklist]
    valueContexts = []
    for enum in valueEnums:
        valueContexts.append({"type": enum.type,
                               "identifier": enumBID(enum),
                               "name": enum.name,
                               "value": enum.value,
                               "supported": supportedLambda(enum) })
    return valueContexts


class Context:

    # TODO-LW document arguments
    # structure:
    # { "items": [ { "item": {...},
    #                "last": <bool>} ],
    #   "firstItem": {...},
    #   "count": <uint>,
    #   "empty": <bool>,
    #   "singleItem": <bool>,
    #   "multipleItems": <bool> }
    @staticmethod
    def listContext(contextList, sortKey=None, filter=lambda i: True):

        context = {}
        if sortKey is not None:
            contextList = sorted(contextList, key=sortKey)

        context["items"] = [{"item": item, "last": item == contextList[-1]}
                            for item in contextList if filter(item)]

        context["firstItem"] = context["items"][0]["item"] if context["items"] else None

        context["count"] = len(context["items"])
        context["empty"] = len(context["items"]) == 0

        context["singleItem"] = len(context["items"]) == 1
        context["multipleItems"] = len(context["items"]) > 1

        return context

    @staticmethod
    def groupItems(items, groupKey, groupKeyList=[], filter=lambda i: True):
        groupMap = {key: [] for key in groupKeyList}
        for item in items:
            if filter(item):
                for gKey in groupKey(item):
                    if gKey not in groupMap:
                        groupMap[gKey] = []
                    groupMap[gKey].append(item)
        return groupMap

    # TODO-LW document arguments
    # structure:
    # { "groups": [ { "name": <string>,
    #                 "items": [ { "item": {...},
    #                              "last": <bool>},
    #                              "hasPrimary": <bool>,
    #                              "isPrimary": <bool>,
    #                              "isSecondary": <bool> } ],
    #                 "firstItem": {...},
    #                 "count": <uint>,
    #                 "empty": <bool>,
    #                 "singleItem": <bool>,
    #                 "multipleItems": <bool>,
    #                 "last": <bool> } ],
    #   "count": <uint>,
    #   "empty": <bool>,
    #   "singleGroup": <bool>,
    #   "multipleGroups": <bool> }
    @classmethod
    def groupedContext(_class, contextList, groupKey, primaryGroupKey=None,
                       groupKeyList=[],
                       groupSortKey=None, itemSortKey=None,
                       groupName=lambda gk: str(gk), filter=lambda i: True):
        context = {}
        groupMap = _class.groupItems(contextList, groupKey, groupKeyList, filter)

        groupKeys = list(groupMap.keys())
        if groupSortKey is not None:
            groupKeys.sort(key=groupSortKey)

        context["groups"] = []
        for key in groupKeys:
            if itemSortKey is not None:
                groupMap[key].sort(key=itemSortKey)

            items = []
            for item in groupMap[key]:
                hasPrimary = primaryGroupKey is not None and primaryGroupKey(item) in groupKeys
                isPrimary = primaryGroupKey is not None and primaryGroupKey(item) == key
                items.append({"item": item,
                              "last": item == groupMap[key][-1],
                              "hasPrimary": hasPrimary,
                              "isPrimary": isPrimary,
                              "isSecondary": hasPrimary and not isPrimary})

            context["groups"].append({"name": groupName(key),
                                      "items": items,
                                      "firstItem": items[0]["item"] if items else None,
                                      "count": len(items),
                                      "empty": len(items) == 0,
                                      "singleItem": len(items) == 1,
                                      "multipleItems": len(items) > 1,
                                      "last": key == groupKeys[-1]})
        context["count"] = len(context["groups"])
        context["empty"] = len(context["groups"]) == 0
        context["singleGroup"] = len(context["groups"]) == 1
        context["multipleGroups"] = len(context["groups"]) > 1
        return context

    @staticmethod
    def _listApiMemberSets(minCoreVersion, features):
        apiMemberSetList = []
        for f in features:
            apiMemberSetList.append((f, False, False))
            apiMemberSetList.append((f, False, True))
            if minCoreVersion and (
                    f.major > minCoreVersion[0] or (f.major == minCoreVersion[0] and f.minor >= minCoreVersion[1])):
                apiMemberSetList.append((f, True, False))
        return apiMemberSetList

    def __init__(self, api, multiContextBinding, minCoreVersion, boolean8, revision, features, extensions, enums,
                 bitfGroups, types, commands):
        self.api = api
        self.multiContextBinding = multiContextBinding
        self.boolean8 = boolean8
        self.revision = revision
        self.features = features
        self.extensions = extensions
        self.enums = enums
        self.bitfGroups = bitfGroups
        self.types = types
        self.commands = commands

        self.apiMemberSetList = self._listApiMemberSets(minCoreVersion, features)

        import gen_extensions
        import gen_booleans
        import gen_values
        import gen_types
        import gen_bitfields
        import gen_enums
        import gen_functions
        import gen_features

        self.extensionContexts = gen_extensions.genExtensionContexts(extensions)
        self.booleanContexts = gen_booleans.genBooleanContexts(enums)
        self.valueContexts = gen_values.genValueContexts(enums)
        self.typeContexts = gen_types.genTypeContexts(types, bitfGroups, api)
        self.bitfieldContexts = gen_bitfields.genBitfieldContexts(enums, bitfGroups)
        self.enumContexts = gen_enums.genEnumContexts(enums)
        self.functionContexts = gen_functions.genFunctionContexts(commands)
        self.featureContexts = gen_features.genFeatureContexts(features)

    def apiMemberSets(self):
        return self.apiMemberSetList

    def general(self):

        context = {"api": self.api,
                   "ucapi": self.api.upper(),
                   "binding": self.api + "binding",
                   "ucbinding": (self.api + "binding").upper(),
                   "memberSet": "",
                   "revision": self.revision,
                   "additionalTypeIncludes": self.additionalTypeIncludes(),
                   "additionalTypes": self.additionalTypes(),
                   "bitfieldType": "EGLbitfield" if self.api == "egl" else "GLbitfield",
                   "enumType": "EGLenum" if self.api == "egl" else "GLenum",
                   "booleanType": "EGLBoolean" if self.api == "egl" else "GLboolean",
                   "extensionType": "EGLextension" if self.api == "egl" else "GLextension",
                   "bindingType": "MultiContextBinding" if self.multiContextBinding else "SingleContextBinding",
                   "glapi": self.api.startswith("gl"),
                   "boolean8": self.boolean8,
                   "boolean32": not self.boolean8
                   }

        context["apiMemberSets"] = self.listContext([{"memberSet": versionBID(feature, core, ext)}
                                                     for feature, core, ext in
                                                     ([(None, False, False)] + self.apiMemberSetList)])
        context["extensions"] = self.listContext(self.extensionContexts, sortKey=lambda e: e["identifier"])
        extensionsByCommands = self.groupItems(self.extensionContexts,
                                               groupKey=lambda e: [i["item"]["identifier"] for i in
                                                                   e["reqCommands"]["items"]])
        extensionsByCommandsContexts = [
            {"command": c, "extensions": self.listContext(extensionsByCommands[c], sortKey=lambda e: e["identifier"])}
            for c in extensionsByCommands.keys()]
        context["extensionsByCommandsByInitial"] = self.groupedContext(extensionsByCommandsContexts,
                                                                       groupKey=lambda e: [
                                                                           alphabeticalGroupKey(e["command"],
                                                                                                "egl" if self.api == "egl" else "gl")],
                                                                       groupKeyList=alphabeticalGroupKeys(),
                                                                       groupSortKey=lambda i: str(i),
                                                                       itemSortKey=lambda e: e["command"])
        # TODO-LW: use extensions instead of extensionsIncore for Meta_ReqVersionsByExtension.cpp
        context["extensionsIncore"] = self.listContext(self.extensionContexts,
                                                       filter=lambda e: e["incore"],
                                                       sortKey=lambda e: (e["incoreMajor"] if e["incoreMajor"] else 0,
                                                                          e["incoreMinor"] if e["incoreMinor"] else 0))
        context["extensionsByInitial"] = self.groupedContext(self.extensionContexts,
                                                             groupKey=lambda e: [alphabeticalGroupKey(e["identifier"],
                                                                                                      "EGL_" if self.api == "egl" else "GL_")],
                                                             groupKeyList=alphabeticalGroupKeys(),
                                                             groupSortKey=lambda k: k,
                                                             itemSortKey=lambda e: e["identifier"])
        context["booleans"] = self.listContext(self.booleanContexts, sortKey=lambda e: e["identifier"])
        context["valuesByType"] = self.groupedContext(self.valueContexts, groupKey=lambda e: [e["type"]])
        context["types"] = self.listContext(
            self.typeContexts)  # no sortKey because order by genTypeContexts() should be kept
        context["bitfields"] = self.listContext(self.bitfieldContexts, sortKey=lambda b: b["value"])
        context["bitfieldsByGroup"] = self.groupedContext(self.bitfieldContexts,
                                                          groupKey=lambda b: [i["item"] for i in b["groups"]["items"]],
                                                          primaryGroupKey=lambda b: b["primaryGroup"],
                                                          groupSortKey=lambda g: g,
                                                          itemSortKey=lambda b: b["value"])
        context["bitfieldsByInitial"] = self.groupedContext(self.bitfieldContexts,
                                                            groupKey=lambda b: [alphabeticalGroupKey(b["identifier"],
                                                                                                     "EGL_" if self.api == "egl" else "GL_")],
                                                            groupKeyList=alphabeticalGroupKeys(),
                                                            groupSortKey=lambda k: k,
                                                            itemSortKey=lambda b: b["identifier"])
        context["bitfieldGroups"] = self.listContext([g.name for g in self.bitfGroups], sortKey=lambda g: g)
        context["enums"] = self.listContext(self.enumContexts, sortKey=lambda e: e["value"])
        context["enumsByGroup"] = self.groupedContext(self.enumContexts,
                                                      groupKey=lambda e: [i["item"] for i in e["groups"]["items"]],
                                                      primaryGroupKey=lambda e: e["primaryGroup"],
                                                      groupSortKey=lambda g: g,
                                                      itemSortKey=lambda e: e["value"])
        context["enumsByValue"] = self.groupedContext(self.enumContexts,
                                                      groupKey=lambda e: [
                                                          0 if re.match(".*(CAST|GLX).*", e["value"]) else int(
                                                              e["value"], 0)],
                                                      groupSortKey=lambda g: g,
                                                      itemSortKey=lambda e: (
                                                      enumSuffixPriority(e["identifier"]), e["identifier"]))
        context["enumsByInitial"] = self.groupedContext(self.enumContexts,
                                                        groupKey=lambda e: [alphabeticalGroupKey(e["identifier"],
                                                                                                 "EGL_" if self.api == "egl" else "GL_")],
                                                        groupKeyList=alphabeticalGroupKeys(),
                                                        groupSortKey=lambda k: k,
                                                        itemSortKey=lambda e: e["identifier"])
        context["functions"] = self.listContext(self.functionContexts, sortKey=lambda f: f["identifier"])
        context["functionsByInitial"] = self.groupedContext(self.functionContexts,
                                                            groupKey=lambda f: [alphabeticalGroupKey(f["identifier"],
                                                                                                     "egl" if self.api == "egl" else "gl")],
                                                            groupKeyList=alphabeticalGroupKeys(),
                                                            groupSortKey=lambda k: k,
                                                            itemSortKey=lambda f: f["identifier"])
        context["features"] = self.listContext(self.featureContexts)
        context["latestFeature"] = context["features"]["items"][-1]["item"]

        return context

    def apiMemberSetSpecific(self, feature, core, ext):
        context = {"api": self.api,
                   "ucapi": self.api.upper(),
                   "memberSet": versionBID(feature, core, ext),
                   "revision": self.revision}

        context["booleans"] = self.listContext(self.booleanContexts, sortKey=lambda e: e["identifier"])
        context["valuesByType"] = self.groupedContext(self.valueContexts, groupKey=lambda v: [v["type"]],
                                                      groupSortKey=lambda t: t,
                                                      itemSortKey=lambda v: v["value"],
                                                      filter=lambda v: v["supported"](feature, core, ext))
        context["types"] = self.listContext(
            self.typeContexts)  # no sortKey because order by genTypeContexts() should be kept
        context["bitfields"] = self.listContext(self.bitfieldContexts, sortKey=lambda b: b["value"],
                                                filter=lambda b: b["supported"](feature, core, ext))
        context["enumsByGroup"] = self.groupedContext(self.enumContexts,
                                                      groupKey=lambda e: [i["item"] for i in e["groups"]["items"]],
                                                      primaryGroupKey=lambda e: e["primaryGroup"],
                                                      groupSortKey=lambda g: g,
                                                      itemSortKey=lambda b: b["value"],
                                                      filter=lambda e: e["supported"](feature, core, ext))
        context["functions"] = self.listContext(self.functionContexts, sortKey=lambda f: f["identifier"],
                                                filter=lambda f: f["supported"](feature, core, ext))

        return context

    def additionalTypeIncludes(self):
        if self.api == "gl":
            return ""
        else:
            return "#include <KHR/khrplatform.h>"

    def additionalTypes(self):
        if self.api == "gl":
            return ""
        else:
            return "using EGLint = int;\nusing EGLchar = char;\nusing EGLNativeDisplayType = void*;\nusing EGLNativePixmapType = void*;\nusing EGLNativeWindowType = void*;"


class Generator:
    renderer = None

    @classmethod
    def generate(_class, context, outputPath, templateName=None):
        if _class.renderer is None:
            _class.renderer = pystache.Renderer(search_dirs=os.path.join(execDir, templateDir),
                                                file_extension=templateExtension,
                                                escape=lambda u: u)

        outputDir = os.path.dirname(outputPath).format(**context)

        if not os.path.exists(outputDir):
            os.makedirs(outputDir)

        outputFile = os.path.basename(outputPath)
        outputFile = outputFile.format(**context)
        if templateName is None:
            templateName = outputFile
        else:
            templateName = templateName.format(**context)

        print("generating {} in {}".format(outputFile, outputDir))  # TODO-LW move logging to appropriate place

        with open(os.path.join(outputDir, outputFile), 'w') as file:
            file.write(_class.renderer.render_name(templateName, context))


class Status:
    targetdir = ""


def status(file):
    print("generating " + file.replace(Status.targetdir, ""))


# enum_binding_name_exceptions = [ "DOMAIN", "MAX_VERTEX_TEXTURE_IMAGE_UNITS_ARB", "FALSE", "TRUE", "NO_ERROR", "WAIT_FAILED" ]

def enumBID(enum):
    return enum.name


# extension_binding_name_exceptions = [ ]

# ToDo: discuss - just use name for glbinding?
def extensionBID(extension):
    return extension.name


def functionBID(function):
    return function.name


def alphabeticallyGroupedLists():
    # create a dictionary of lists by upper case letters
    # and a single "everythingelse" list

    keys = '0ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lists = dict()
    for key in keys:
        lists[key] = list()

    return lists


def alphabeticalGroupKeys():
    return [str(c) for c in "0ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


def alphabeticalGroupKey(identifier, prefix):
    # derives an key from an identifier with prefix

    index = identifier.find(prefix)
    if index < 0:
        return -1

    index += len(prefix)

    key = ((identifier[index:])[:1]).upper()
    if ord(key) not in range(65, 91):
        key = '0'

    return key


class CPPGenerator:
    def generate(profile, api):
        profile.baseNamespace
        multiContextBinding = profile.multiContextBinding
        booleanWidth = profile.booleanWidth
        bindingNamespace = profile.bindingNamespace
        minCoreVersion = profile.minCoreVersion
        targetdir = profile.targetDir

        includedir = pjoin(targetdir, pjoin(bindingNamespace, "include/" + bindingNamespace + "/"))
        includedir_api = pjoin(includedir, "{api}{memberSet}/")
        includedir_aux = pjoin(targetdir, pjoin(bindingNamespace + "-aux", "include/" + bindingNamespace + "-aux/"))
        sourcedir = pjoin(targetdir, pjoin(bindingNamespace, "source/"))
        sourcedir_api = pjoin(sourcedir, "{api}/")
        sourcedir_aux = pjoin(targetdir, pjoin(bindingNamespace + "-aux", "source/"))
        testdir = pjoin(targetdir, "tests/" + bindingNamespace + "-test/")

        context = Context(profile.baseNamespace, multiContextBinding, minCoreVersion, booleanWidth == 8, api.revision, api.versions, api.extensions,
                          api.constants, None, api.types, api.functions)
        generalContext = context.general()

        generateBegin = time.time()

        # Generate files with common context
        Generator.generate(generalContext, pjoin(sourcedir_aux, "{api}revision.h"))
        Generator.generate(generalContext, pjoin(includedir_api, "extension.h"))
        # Generator.generate(generalContext, pjoin(includedir_api, "boolean.h"))
        Generator.generate(generalContext, pjoin(includedir_api, "values.h"))
        Generator.generate(generalContext, pjoin(includedir_api, "types.h"))
        Generator.generate(generalContext, pjoin(includedir_api, "bitfield.h"))
        Generator.generate(generalContext, pjoin(includedir_api, "enum.h"))
        Generator.generate(generalContext, pjoin(includedir_api, "functions.h"))
        Generator.generate(generalContext, pjoin(includedir_api, "{api}.h"))

        Generator.generate(generalContext, pjoin(testdir, "AllVersions_test.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "ValidVersions_list.cpp"))

        Generator.generate(generalContext, pjoin(includedir_aux, "Meta.h"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_Maps.h"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_getStringByBitfield.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_StringsByBitfield.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_BitfieldsByString.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_StringsByBoolean.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_BooleansByString.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_StringsByEnum.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_EnumsByString.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_StringsByExtension.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_ExtensionsByString.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_ReqVersionsByExtension.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_FunctionStringsByExtension.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_FunctionStringsByVersion.cpp"))
        Generator.generate(generalContext, pjoin(sourcedir_aux, "Meta_ExtensionsByFunctionString.cpp"))

        # KHR binding

        if multiContextBinding:
            Generator.generate(generalContext, pjoin(includedir, "Binding.h"), "khrbinding/MultiContextBinding.h")
            Generator.generate(generalContext, pjoin(sourcedir, "Binding.cpp"), "khrbinding/MultiContextBinding.cpp")
            Generator.generate(generalContext, pjoin(includedir, bindingNamespace + ".h"),
                               "khrbinding/multicontextinterface.h")
            Generator.generate(generalContext, pjoin(sourcedir, bindingNamespace + ".cpp"),
                               "khrbinding/multicontextinterface.cpp")
        else:
            Generator.generate(generalContext, pjoin(includedir, "Binding.h"), "khrbinding/SingleContextBinding.h")
            Generator.generate(generalContext, pjoin(sourcedir, "Binding.cpp"), "khrbinding/SingleContextBinding.cpp")
            Generator.generate(generalContext, pjoin(includedir, bindingNamespace + ".h"),
                               "khrbinding/singlecontextinterface.h")
            Generator.generate(generalContext, pjoin(sourcedir, bindingNamespace + ".cpp"),
                               "khrbinding/singlecontextinterface.cpp")

        Generator.generate(generalContext, pjoin(sourcedir, "Binding_list.cpp"))

        if booleanWidth == 8:
            Generator.generate(generalContext, pjoin(includedir, "Boolean8.h"), "khrbinding/Boolean8.h")
            Generator.generate(generalContext, pjoin(includedir, "Boolean8.inl"), "khrbinding/Boolean8.inl")
        else:
            Generator.generate(generalContext, pjoin(includedir, "Boolean32.h"), "khrbinding/Boolean32.h")
            Generator.generate(generalContext, pjoin(includedir, "Boolean32.inl"), "khrbinding/Boolean32.inl")

        Generator.generate(generalContext, pjoin(includedir, "AbstractFunction.h"), "khrbinding/AbstractFunction.h")
        Generator.generate(generalContext, pjoin(includedir, "AbstractState.h"), "khrbinding/AbstractState.h")
        Generator.generate(generalContext, pjoin(includedir, "AbstractValue.h"), "khrbinding/AbstractValue.h")
        Generator.generate(generalContext, pjoin(includedir, "CallbackMask.h"), "khrbinding/CallbackMask.h")
        Generator.generate(generalContext, pjoin(includedir, "CallbackMask.inl"), "khrbinding/CallbackMask.inl")
        Generator.generate(generalContext, pjoin(includedir, "ContextHandle.h"), "khrbinding/ContextHandle.h")
        Generator.generate(generalContext, pjoin(includedir, "Function.h"), "khrbinding/Function.h")
        Generator.generate(generalContext, pjoin(includedir, "Function.inl"), "khrbinding/Function.inl")
        Generator.generate(generalContext, pjoin(includedir, "FunctionCall.h"), "khrbinding/FunctionCall.h")
        Generator.generate(generalContext, pjoin(includedir, "ProcAddress.h"), "khrbinding/ProcAddress.h")
        Generator.generate(generalContext, pjoin(includedir, "SharedBitfield.h"), "khrbinding/SharedBitfield.h")
        Generator.generate(generalContext, pjoin(includedir, "SharedBitfield.inl"), "khrbinding/SharedBitfield.inl")
        Generator.generate(generalContext, pjoin(includedir, "State.h"), "khrbinding/State.h")
        Generator.generate(generalContext, pjoin(includedir, "Value.h"), "khrbinding/Value.h")
        Generator.generate(generalContext, pjoin(includedir, "Value.inl"), "khrbinding/Value.inl")
        Generator.generate(generalContext, pjoin(includedir, "Version.h"), "khrbinding/Version.h")
        Generator.generate(generalContext, pjoin(includedir, "Version.inl"), "khrbinding/Version.inl")

        Generator.generate(generalContext, pjoin(sourcedir, "AbstractFunction.cpp"), "khrbinding/AbstractFunction.cpp")
        Generator.generate(generalContext, pjoin(sourcedir, "AbstractState.cpp"), "khrbinding/AbstractState.cpp")
        Generator.generate(generalContext, pjoin(sourcedir, "AbstractValue.cpp"), "khrbinding/AbstractValue.cpp")
        Generator.generate(generalContext, pjoin(sourcedir, "FunctionCall.cpp"), "khrbinding/FunctionCall.cpp")
        Generator.generate(generalContext, pjoin(sourcedir, "State.cpp"), "khrbinding/State.cpp")

        # KHR binding AUX

        Generator.generate(generalContext, pjoin(includedir_aux, "RingBuffer.h"), "khrbinding-aux/RingBuffer.h")
        Generator.generate(generalContext, pjoin(includedir_aux, "RingBuffer.inl"), "khrbinding-aux/RingBuffer.inl")
        Generator.generate(generalContext, pjoin(includedir_aux, "types_to_string.h"),
                           "khrbinding-aux/types_to_string.h")
        Generator.generate(generalContext, pjoin(includedir_aux, "types_to_string.inl"),
                           "khrbinding-aux/types_to_string.inl")
        Generator.generate(generalContext, pjoin(includedir_aux, "ValidVersions.h"), "khrbinding-aux/ValidVersions.h")

        Generator.generate(generalContext, pjoin(sourcedir_aux, "ValidVersions.cpp"),
                           "khrbinding-aux/ValidVersions.cpp")
        Generator.generate(generalContext, pjoin(sourcedir_aux, "types_to_string.cpp"),
                           "khrbinding-aux/types_to_string.cpp")

        # Generate function-related files with specific contexts for each initial letter of the function name
        for functionGroup in generalContext["functionsByInitial"]["groups"]:
            specificContext = generalContext.copy()
            specificContext["currentFunctionGroup"] = functionGroup
            specificContext["currentFunctionInitial"] = functionGroup["name"].lower()

            Generator.generate(specificContext, pjoin(sourcedir_api, "functions_{currentFunctionInitial}.cpp"),
                               "functions.cpp")
            Generator.generate(specificContext, pjoin(sourcedir, "Binding_objects_{currentFunctionInitial}.cpp"),
                               "Binding_objects.cpp")

        # Generate files with ApiMemberSet-specific contexts
        for feature, core, ext in context.apiMemberSets():
            specificContext = context.apiMemberSetSpecific(feature, core, ext)

            Generator.generate(specificContext, pjoin(includedir_api, "boolean.h"), "booleanF.h")
            Generator.generate(specificContext, pjoin(includedir_api, "values.h"), "valuesF.h")
            Generator.generate(specificContext, pjoin(includedir_api, "types.h"), "typesF.h")
            Generator.generate(specificContext, pjoin(includedir_api, "bitfield.h"), "bitfieldF.h")
            Generator.generate(specificContext, pjoin(includedir_api, "enum.h"), "enumF.h")
            Generator.generate(specificContext, pjoin(includedir_api, "functions.h"), "functionsF.h")
            Generator.generate(specificContext, pjoin(includedir_api, "{api}.h"), "{api}F.h")

        generateEnd = time.time()
        print("generation took {:.3f} seconds".format(generateEnd - generateBegin))
