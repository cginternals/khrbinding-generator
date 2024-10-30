
import collections
import os, sys
from os.path import join as pjoin
import time
import re
from itertools import groupby

from jinja2 import Environment, PackageLoader, Template

from khrapi.BitfieldGroup import BitfieldGroup
from khrapi.Enumerator import Enumerator
from khrapi.Version import Version
from khrapi.NativeType import NativeType
from khrapi.TypeAlias import TypeAlias
from khrapi.NativeCode import NativeCode
from khrapi.CompoundType import CompoundType

def performTypeNameNormalization(typeName):
    typeName = typeName.strip()
    if typeName.startswith("const "):
        return performTypeNameNormalization(typeName[6:])
    if typeName.endswith("*"):
        return performTypeNameNormalization(typeName[:-1])
    if typeName.endswith("&"):
        return performTypeNameNormalization(typeName[:-1])
    return typeName

def getMinCoreVersionsLookup(profile):
    splitMajorMinor = lambda version: { "major": int(version.split(".")[0]), "minor": int(version.split(".")[1]) }
    return { identifier: splitMajorMinor(api["coreProfileSince"]) for identifier, api in profile.apis.items() if "coreProfileSince" in api }

class CPPGenerator:

    @classmethod
    def ensure_dir(cls, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    @classmethod
    def render(cls, engine, template, target, **kwargs):
        templateFilename = Template(template).render(**kwargs)
        targetFilename = Template(target).render(**kwargs)
        cls.ensure_dir(targetFilename)
        print("Generate %s" % (targetFilename))
        t = engine.get_template(templateFilename)
        t.stream(**kwargs).dump(targetFilename)

    @classmethod
    def generate(cls, profile, api, binding):
        targetdir = profile.targetDir

        # TEMPLATE SETUP

        template_engine = Environment(loader=PackageLoader('khrgenerator.cpp', 'templates'))

        # target directory structure

        includedir = pjoin(targetdir, pjoin(binding.identifier, "include/" + binding.identifier + "/"))
        includedir_api = pjoin(includedir, "{{apiString}}{{memberSet}}/")
        includedir_aux = pjoin(targetdir, pjoin(binding.bindingAuxIdentifier, "include", binding.bindingAuxIdentifier+"/"))
        sourcedir = pjoin(targetdir, pjoin(binding.identifier, "source/"))
        sourcedir_api = pjoin(sourcedir, "{{binding.baseNamespace}}/")
        sourcedir_aux = pjoin(targetdir, pjoin(binding.bindingAuxIdentifier, "source/"))
        testdir = pjoin(targetdir, "tests/" + binding.identifier + "-test/")

        booleanTypes = [ type for type in api.types if type.identifier == profile.booleanType and isinstance(type, Enumerator) ]
        booleanValues = [ constant for booleanType in booleanTypes for constant in booleanType.values ]
        booleanValueNames = [ constant.identifier for constant in booleanValues ]

        enumTypes = [ type for type in api.types if isinstance(type, Enumerator) and type.identifier != profile.booleanType and type.identifier != profile.extensionType ]
        enumConstants = [ constant for constant in api.constants if len(constant.groups) > 0 and constant.groups[0] in enumTypes ]
        originalEnumTypes = [ type for type in enumTypes if type.hideDeclaration ]
        enumTypes = [ type for type in enumTypes if not type.hideDeclaration ]

        bitfieldTypes = [ type for type in api.types if isinstance(type, BitfieldGroup) ]
        bitfieldConstants = [ constant for constant in api.constants if len(constant.groups) > 0 and constant.groups[0] in bitfieldTypes ]

        # TEMPLATE APPLICATION

        # API binding

        cls.render(template_engine, "extension.h", includedir_api+"extension.h", api=api, profile=profile, binding=binding, apiString=binding.baseNamespace)
        cls.render(template_engine, "boolean.h", includedir_api+"boolean.h", api=api, profile=profile, binding=binding, apiString=binding.baseNamespace,
            values=booleanValues,
            nativeType="Boolean8" if binding.booleanWidth == 8 else "Boolean32"
        )
        cls.render(template_engine, "values.h", includedir_api+"values.h", api=api, profile=profile, binding=binding, apiString=binding.baseNamespace,
            values=api.typeByIdentifier("SpecialValues")
        )
        cls.render(template_engine, "types.h", includedir_api+"types.h", api=api, profile=profile, binding=binding, apiString=binding.baseNamespace,
            platform_includes=[ type.moduleName for type in api.dependencies if not type.hideDeclaration ],
            undefs=binding.undefs,
            types= [
                { 'identifier': type.identifier,
                  'declaration': Template(declaration).render(binding=binding),
                  'relevance': cls.getTypeRelevance(type)
                } for type, declaration in [ (type, cls.getDeclaration(type)) for type in api.types ] if len(declaration) > 0
            ]
        )
        cls.render(template_engine, "types.inl", includedir_api+"types.inl", api=api, profile=profile, binding=binding, apiString=binding.baseNamespace,
            basic_enumerators=[ type for type in [ api.typeByIdentifier(binding.extensionType) ] if type is not None ],
            generic_enumerators=[ type for type in [ api.typeByIdentifier(binding.enumType) ] if type is not None ],
            bitfields=bitfieldTypes
        )
        cls.render(template_engine, "bitfield.h", includedir_api+"bitfield.h", api=api, profile=profile, binding=binding, apiString=binding.baseNamespace,
            groups=bitfieldTypes,
            constants=bitfieldConstants,
            max_constant_length=str(max([ len(constant.identifier) for constant in bitfieldConstants ] + [ 0 ]))
        )
        cls.render(template_engine, "enum.h", includedir_api+"enum.h", api=api, profile=profile, binding=binding, apiString=binding.baseNamespace,
            groups= enumTypes if binding.useEnumGroups else originalEnumTypes,
            constants=enumConstants,
            max_constant_length=str(max([ len(constant.identifier) for constant in enumConstants ] + [ 0 ]))
        )
        cls.render(template_engine, "functions.h", includedir_api+"functions.h", api=api, profile=profile, binding=binding, apiString=binding.baseNamespace,
            functions=[ function for function in api.functions ]
        )
        cls.render(template_engine, "entrypoint.h", includedir_api+"{{binding.baseNamespace}}.h", api=api, profile=profile, binding=binding, apiString=binding.baseNamespace)

        cls.render(template_engine, "AllVersions_test.cpp", testdir+"AllVersions_test.cpp", api=api, profile=profile, binding=binding,
            versions=api.versions
        )
        cls.render(template_engine, "exclusion.h", includedir+"no{{binding.baseNamespace}}.h", api=api, profile=profile, binding=binding)

        ## KHR binding

        if binding.multiContextBinding:
            cls.render(template_engine, "khrbinding/MultiContextBinding.h", includedir+"Binding.h", api=api, profile=profile, binding=binding,
                functions=api.functions
            )
            cls.render(template_engine, "khrbinding/MultiContextBinding.cpp", sourcedir+"Binding.cpp", api=api, profile=profile, binding=binding)
            cls.render(template_engine, "khrbinding/multicontextinterface.h", includedir+"{{binding.namespace}}.h", api=api, profile=profile, binding=binding)
            cls.render(template_engine, "khrbinding/multicontextinterface.cpp", sourcedir+"{{binding.namespace}}.cpp", api=api, profile=profile, binding=binding)
        else:
            cls.render(template_engine, "khrbinding/SingleContextBinding.h", includedir+"Binding.h", api=api, profile=profile, binding=binding,
                functions=api.functions
            )
            cls.render(template_engine, "khrbinding/SingleContextBinding.cpp", sourcedir+"Binding.cpp", api=api, profile=profile, binding=binding)
            cls.render(template_engine, "khrbinding/singlecontextinterface.h", includedir+"{{binding.namespace}}.h", api=api, profile=profile, binding=binding)
            cls.render(template_engine, "khrbinding/singlecontextinterface.cpp", sourcedir+"{{binding.namespace}}.cpp", api=api, profile=profile, binding=binding)

        cls.render(template_engine, "Binding_list.cpp", sourcedir+"Binding_list.cpp", api=api, profile=profile, binding=binding,
            functions=api.functions
        )

        if binding.booleanWidth == 8:
            cls.render(template_engine, "khrbinding/Boolean8.h", includedir+"Boolean8.h", api=api, profile=profile, binding=binding)
            cls.render(template_engine, "khrbinding/Boolean8.inl", includedir+"Boolean8.inl", api=api, profile=profile, binding=binding)
        else:
            cls.render(template_engine, "khrbinding/Boolean32.h", includedir+"Boolean32.h", api=api, profile=profile, binding=binding)
            cls.render(template_engine, "khrbinding/Boolean32.inl", includedir+"Boolean32.inl", api=api, profile=profile, binding=binding)

        cls.render(template_engine, "khrbinding/AbstractFunction.h", includedir+"AbstractFunction.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/AbstractState.h", includedir+"AbstractState.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/AbstractValue.h", includedir+"AbstractValue.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/CallbackMask.h", includedir+"CallbackMask.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/CallbackMask.inl", includedir+"CallbackMask.inl", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/ContextHandle.h", includedir+"ContextHandle.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/Function.h", includedir+"Function.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/Function.inl", includedir+"Function.inl", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/FunctionCall.h", includedir+"FunctionCall.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/ProcAddress.h", includedir+"ProcAddress.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/SharedBitfield.h", includedir+"SharedBitfield.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/SharedBitfield.inl", includedir+"SharedBitfield.inl", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/State.h", includedir+"State.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/Value.h", includedir+"Value.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/Value.inl", includedir+"Value.inl", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/Version.h", includedir+"Version.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/Version.inl", includedir+"Version.inl", api=api, profile=profile, binding=binding)

        cls.render(template_engine, "khrbinding/AbstractFunction.cpp", sourcedir+"AbstractFunction.cpp", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/AbstractState.cpp", sourcedir+"AbstractState.cpp", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/AbstractValue.cpp", sourcedir+"AbstractValue.cpp", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/FunctionCall.cpp", sourcedir+"FunctionCall.cpp", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding/State.cpp", sourcedir+"State.cpp", api=api, profile=profile, binding=binding)

        ## KHR binding AUX

        cls.render(template_engine, "revision.h", sourcedir_aux+"{{binding.baseNamespace}}revision.h", api=api, profile=profile, binding=binding)

        cls.render(template_engine, "ValidVersions_list.cpp", sourcedir_aux+"ValidVersions_list.cpp", api=api, profile=profile, binding=binding,
            versions=[ version for version in api.versions if isinstance(version, Version) ]
        )

        cls.render(template_engine, "Meta.h", includedir_aux+"Meta.h", api=api, profile=profile, binding=binding,
            bitfieldGroups=bitfieldTypes,
            enumGroups=enumTypes
        )
        cls.render(template_engine, "Meta_Maps.h", sourcedir_aux+"Meta_Maps.h", api=api, profile=profile, binding=binding,
            bitfieldGroups=bitfieldTypes,
            enumGroups=originalEnumTypes if binding.useEnumGroups else []
        )
        cls.render(template_engine, "Meta_getStringByBitfield.cpp", sourcedir_aux+"Meta_getStringByBitfield.cpp", api=api, profile=profile, binding=binding,
            groups=bitfieldTypes
        )
        cls.render(template_engine, "Meta_StringsByBitfield.cpp", sourcedir_aux+"Meta_StringsByBitfield.cpp", api=api, profile=profile, binding=binding,
            groups=bitfieldTypes
        )
        cls.render(template_engine, "Meta_BitfieldsByString.cpp", sourcedir_aux+"Meta_BitfieldsByString.cpp", api=api, profile=profile, binding=binding,
            groups=cls.identifierPrefixGroups(api, bitfieldConstants, len(profile.uppercasePrefix))
        )
        cls.render(template_engine, "Meta_StringsByBoolean.cpp", sourcedir_aux+"Meta_StringsByBoolean.cpp", api=api, profile=profile, binding=binding,
            booleans=booleanValues
        )
        cls.render(template_engine, "Meta_BooleansByString.cpp", sourcedir_aux+"Meta_BooleansByString.cpp", api=api, profile=profile, binding=binding,
            booleans=booleanValues
        )
        cls.render(template_engine, "Meta_StringsByEnum.cpp", sourcedir_aux+"Meta_StringsByEnum.cpp", api=api, profile=profile, binding=binding,
            constants=enumConstants
        )
        cls.render(template_engine, "Meta_EnumsByString.cpp", sourcedir_aux+"Meta_EnumsByString.cpp", api=api, profile=profile, binding=binding,
            groups=cls.identifierPrefixGroups(api, enumConstants, len(profile.uppercasePrefix))
        )
        cls.render(template_engine, "Meta_StringsByExtension.cpp", sourcedir_aux+"Meta_StringsByExtension.cpp", api=api, profile=profile, binding=binding,
            extensions=api.extensions
        )
        cls.render(template_engine, "Meta_ExtensionsByString.cpp", sourcedir_aux+"Meta_ExtensionsByString.cpp", api=api, profile=profile, binding=binding,
            groups=cls.identifierPrefixGroups(api, api.extensions, len(profile.uppercasePrefix))
        )
        cls.render(template_engine, "Meta_ReqVersionsByExtension.cpp", sourcedir_aux+"Meta_ReqVersionsByExtension.cpp", api=api, profile=profile, binding=binding,
            extensionsInCore=api.extensionsByCoreVersion()
        )
        cls.render(template_engine, "Meta_FunctionStringsByExtension.cpp", sourcedir_aux+"Meta_FunctionStringsByExtension.cpp", api=api, profile=profile, binding=binding,
            extensions=api.extensions
        )
        cls.render(template_engine, "Meta_FunctionStringsByVersion.cpp", sourcedir_aux+"Meta_FunctionStringsByVersion.cpp", api=api, profile=profile, binding=binding,
            versions=[ version for version in api.versions if isinstance(version, Version) ]
        )
        cls.render(template_engine, "Meta_ExtensionsByFunctionString.cpp", sourcedir_aux+"Meta_ExtensionsByFunctionString.cpp", api=api, profile=profile, binding=binding,
            extensionsByFunction=cls.identifierPrefixGroupsDict(api, api.extensionsByFunction(), len(profile.lowercasePrefix))
        )

        uniqueEnumTypes = []
        for type in [ api.typeByIdentifier(binding.extensionType), api.typeByIdentifier(binding.enumType), api.typeByIdentifier(binding.booleanType) ]:
            if type not in enumTypes and type not in uniqueEnumTypes and type is not None:
                uniqueEnumTypes.append(type)
        
        cls.render(template_engine, "khrbinding-aux/RingBuffer.h", includedir_aux+"RingBuffer.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding-aux/RingBuffer.inl", includedir_aux+"RingBuffer.inl", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding-aux/types_to_string.h", includedir_aux+"types_to_string.h", api=api, profile=profile, binding=binding,
            enumerators=enumTypes,
            uniqueEnumerators=uniqueEnumTypes,
            bitfields=bitfieldTypes,
            cStringTypes=binding.cStringOutputTypes,
        )
        cls.render(template_engine, "khrbinding-aux/types_to_string.inl", includedir_aux+"types_to_string.inl", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding-aux/types_to_string.cpp", sourcedir_aux+"types_to_string.cpp", api=api, profile=profile, binding=binding,
            enumerators=enumTypes,
            uniqueEnumerators=uniqueEnumTypes,
            bitfields=bitfieldTypes,
            cStringTypes=binding.cStringOutputTypes,
            cPointerTypes=binding.cPointerTypes,
            nativeTypes=[ "int", "unsigned int", "float", "char", "unsigned char", "long", "unsigned long", "long long", "unsigned long long", "double"],
            types=[ type for type in api.types if not type.hideDeclaration and not type.declaration.startswith('struct') and not type.identifier in binding.cPointerTypes and not isinstance(type, NativeCode) and not isinstance(type, CompoundType) and not isinstance(type, TypeAlias) ]
        )
        
        cls.render(template_engine, "khrbinding-aux/ValidVersions.h", includedir_aux+"ValidVersions.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding-aux/ValidVersions.cpp", sourcedir_aux+"ValidVersions.cpp", api=api, profile=profile, binding=binding)

        # Caching source files

        groupedFunctions = cls.identifierPrefixGroups(api, api.functions, len(profile.lowercasePrefix))
        for prefix in cls.prefixes(api):
            cls.render(template_engine, "functions.cpp", sourcedir_api+"functions_{{prefix|lower}}.cpp", api=api, profile=profile, binding=binding,
                prefix=prefix,
                functions=groupedFunctions[prefix]
            )
            cls.render(template_engine, "Binding_objects.cpp", sourcedir+"Binding_objects_{{prefix|lower}}.cpp", api=api, profile=profile, binding=binding,
                prefix=prefix,
                functions=groupedFunctions[prefix]
            )

        # Generate files with ApiMemberSet-specific contexts
        availableConstants = set(api.constants)
        availableFunctions = set(api.functions)
        currentConstants = set()
        currentFunctions = set()
        deprecatedConstants = set()
        deprecatedFunctions = set()
        removedConstants = set()
        removedFunctions = set()
        currentFeature = None
        specialValueType = api.typeByIdentifier("SpecialValues")
        apiIdentifier = ""
        for feature, core, ext in cls.apiMemberSets(api, profile, api.versions):
            if apiIdentifier != feature.apiIdentifier:
                currentConstants = set()
                currentFunctions = set()
                deprecatedConstants = set()
                deprecatedFunctions = set()
                removedConstants = set()
                removedFunctions = set()
                apiIdentifier = feature.apiIdentifier
                
            if currentFeature != feature: # apply changes
                currentConstants |= set(feature.requiredConstants)
                currentFunctions |= set(feature.requiredFunctions)
                currentConstants -= set(feature.deprecatedConstants)
                currentFunctions -= set(feature.deprecatedFunctions)
                currentConstants -= set(feature.removedConstants)
                currentFunctions -= set(feature.removedFunctions)
                deprecatedConstants |= set(feature.deprecatedConstants)
                deprecatedFunctions |= set(feature.deprecatedFunctions)
                deprecatedConstants -= set(feature.removedConstants)
                deprecatedFunctions -= set(feature.removedFunctions)
                removedConstants |= set(feature.removedConstants)
                removedFunctions |= set(feature.removedFunctions)
                currentFeature = feature

            memberSet = "%i%i%s%s" % (feature.majorVersion, feature.minorVersion, "core" if core else "", "ext" if ext else "")

            if core:
                constants = currentConstants
                functions = currentFunctions
            elif ext and profile.stripFeatureHeaders:
                # Filter away functions and constants from the main specification and from extensions not supported by the current API.
                # TODO: This filters away extensions not supported by the API, but the versioned headers can still contain bindings for extension not supported by current version.
                # Unfortunately, the API version required by the different extensions is only detailed in the different extension specifications and not the API specification XML.
                # To further scope down the extensions to only the supported ones the extension specification XML files should be downloaded and parsed from the Khronos registry
                # as well (https://registry.khronos.org/OpenGL/extensions).
                supportedExtensions = [ extension for extension in api.extensions if len(extension.supportedAPIs) == 0 or (apiIdentifier and apiIdentifier in extension.supportedAPIs) ]
                constants = set()
                functions = set()
                for extension in supportedExtensions:
                    constants |= set(extension.requiredConstants)
                    functions |= set(extension.requiredFunctions)

                # Some extensions add functions that are present in the main specification (before they are added to the main specification). Remove these ones
                # as well as they should already be present in the normal or core set.
                constants -= currentConstants
                functions -= currentFunctions
            elif ext:
                constants = availableConstants - currentConstants - deprecatedConstants - removedConstants
                functions = availableFunctions - currentFunctions - deprecatedFunctions - removedFunctions
            else: # normal
                constants = currentConstants | deprecatedConstants
                functions = currentFunctions | deprecatedFunctions

            if profile.stripFeatureHeaders:
                # Determine used types based on required functions and enums
                neededTypes = set(booleanTypes)
                for function in functions:
                    if function.returnType:
                        type = api.typeByIdentifier(performTypeNameNormalization(function.returnType.identifier))
                        if type and not type.hideDeclaration and not isinstance(type, NativeCode):
                            neededTypes.add(type)

                    for parameter in function.parameters:
                        type = api.typeByIdentifier(performTypeNameNormalization(parameter.type.identifier))
                        if type and not type.hideDeclaration and not isinstance(type, NativeCode):
                            neededTypes.add(type)

                neededTypes = list(neededTypes)
            else:
                neededTypes = [ type for type in api.types if (not type.hideDeclaration or type in booleanTypes) and not isinstance(type, NativeCode) ]

            cls.render(template_engine, "typesF.h", includedir_api+"types.h", api=api, profile=profile, binding=binding,memberSet=memberSet,apiString=feature.apiString,
                types=neededTypes
            )
            cls.render(template_engine, "booleanF.h", includedir_api+"boolean.h", api=api, profile=profile, binding=binding,memberSet=memberSet,apiString=feature.apiString,
                constants=booleanValues,
            )
            cls.render(template_engine, "bitfieldF.h", includedir_api+"bitfield.h", api=api, profile=profile, binding=binding,memberSet=memberSet,apiString=feature.apiString,
                constants=[ constant for constant in constants if len(constant.groups) > 0 and isinstance(constant.groups[0], BitfieldGroup) ],
            )
            cls.render(template_engine, "enumF.h", includedir_api+"enum.h", api=api, profile=profile, binding=binding,memberSet=memberSet,apiString=feature.apiString,
                constants=[ constant for constant in constants if len(constant.groups) > 0 and isinstance(constant.groups[0], Enumerator) and constant.groups[0].identifier != profile.booleanType ],
            )
            cls.render(template_engine, "valuesF.h", includedir_api+"values.h", api=api, profile=profile, binding=binding,memberSet=memberSet,apiString=feature.apiString,
                values=[ constant for constant in constants if specialValueType is not None and constant.identifier in [ value.identifier for value in specialValueType.values ] ],
            )
            cls.render(template_engine, "functionsF.h", includedir_api+"functions.h", api=api, profile=profile, binding=binding,memberSet=memberSet,apiString=feature.apiString,
                functions=[ function for function in functions ]
            )
            entryPointHeader = profile.apis[feature.apiString]["entryPointHeader"] if feature.apiString in profile.apis.keys() else f"{feature.apiString}.h"
            cls.render(template_engine, "entrypointF.h", includedir_api+"{{entryPointHeader}}", api=api, profile=profile, binding=binding,memberSet=memberSet,apiString=feature.apiString,entryPointHeader=entryPointHeader)

    @classmethod
    def prefixes(cls, api):
        return [ "0" ] + [ chr(alpha) for alpha in range(ord('A'), ord('Z')+1) ]

    @classmethod
    def identifierPrefixGroups(cls, api, values, lookupOffset):
        result = { prefix:[] for prefix in cls.prefixes(api) }
        for value in values:
            result[value.identifier[lookupOffset].upper() if value.identifier[lookupOffset].isalpha() else '0'].append(value)
        return result

    @classmethod
    def identifierPrefixGroupsDict(cls, api, dictionary, lookupOffset):
        result = { prefix:{} for prefix in cls.prefixes(api) }
        for key, values in dictionary.items():
            result[key.identifier[lookupOffset].upper() if key.identifier[lookupOffset].isalpha() else '0'][key] = values
        return result

    @classmethod
    def getTypeRelevance(cls, type, resolveAliases=True):
        if type.hideDeclaration:
            return -1

        if isinstance(type, NativeCode):
            return 0
        if isinstance(type, NativeType):
            if type.declaration.startswith("struct"):
                return 5
            else:
                return 0
        if isinstance(type, TypeAlias):
            if type.identifier.isupper():
                return 4
            if isinstance(type.aliasedType, NativeType):
                return 1
            else:
                return 2
        if isinstance(type, Enumerator):
            return 3
        if isinstance(type, BitfieldGroup):
            return 3
        if isinstance(type, NativeCode):
            return 5
        if isinstance(type, CompoundType):
            return 5
        
        return 6

    @classmethod
    def getDeclaration(cls, type, resolveAliases=True):
        if type.hideDeclaration:
            return ""

        if isinstance(type, NativeType):
            return type.declaration
        if isinstance(type, TypeAlias):
            return "using %s = %s;" % (type.identifier, type.aliasedType.identifier)
        if isinstance(type, Enumerator):
            return "enum class %s : %s;" % (type.identifier, "unsigned int" if type.unsigned else "int")
        if isinstance(type, BitfieldGroup):
            return "enum class %s : unsigned int;" % (type.identifier)
        if isinstance(type, NativeCode):
            return type.declaration
        if isinstance(type, CompoundType):
            if type.type == "struct":
                return "struct %s {\n\t%s\n};" % (type.identifier, "\n\t".join([attribute.type.identifier + " " + attribute.name + ";" for attribute in type.memberAttributes ]))
            elif type.type == "union":
                return "union %s {\n\t%s\n};" % (type.identifier, "\n\t".join([attribute.type.identifier + " " + attribute.name + ";" for attribute in type.memberAttributes ]))
            else:
                pass
        
        return ""

    @classmethod
    def apiMemberSets(cls, api, profile, versions):
        minCoreVersions = getMinCoreVersionsLookup(profile)

        for version in versions:
            if minCoreVersions and version.apiString in minCoreVersions and (minCoreVersions[version.apiString]["major"] < version.majorVersion or minCoreVersions[version.apiString]["major"] <= version.majorVersion and minCoreVersions[version.apiString]["minor"] <= version.minorVersion):
                yield version, False, False
                yield version, True, False
                yield version, False, True
            else:
                yield version, False, False
                yield version, False, True
