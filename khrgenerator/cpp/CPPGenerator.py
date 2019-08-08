
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
from khrapi.Import import Import

class CPPGenerator:

    @classmethod
    def render(cls, engine, template, target, **kwargs):
        templateFilename = Template(template).render(**kwargs)
        targetFilename = Template(target).render(**kwargs)
        print("Generate %s" % (targetFilename))
        t = engine.get_template(templateFilename)
        t.stream(**kwargs).dump(targetFilename)

    @classmethod
    def generate(cls, profile, api, binding):
        targetdir = profile.targetDir

        # TEMPLATE SETUP

        template_engine = Environment(loader=PackageLoader('khrgenerator.cpp', 'templates'))
        # print(template_engine.list_templates())

        # target directory structure

        includedir = pjoin(targetdir, pjoin(binding.identifier, "include/" + binding.identifier + "/"))
        includedir_api = pjoin(includedir, "{{binding.baseNamespace}}{{memberSet}}/")
        includedir_aux = pjoin(targetdir, pjoin(binding.bindingAuxIdentifier, "include", binding.bindingAuxIdentifier+"/"))
        sourcedir = pjoin(targetdir, pjoin(binding.identifier, "source/"))
        sourcedir_api = pjoin(sourcedir, "{{binding.baseNamespace}}/")
        sourcedir_aux = pjoin(targetdir, pjoin(binding.bindingAuxIdentifier, "source/"))
        testdir = pjoin(targetdir, "tests/" + binding.identifier + "-test/")

        # TEMPLATE APPLICATION

        # API binding

        cls.render(template_engine, "extension.h", includedir_api+"extension.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "values.h", includedir_api+"values.h", api=api, profile=profile, binding=binding,
            values=api.typeByIdentifier("SpecialValues")
        )
        cls.render(template_engine, "types.h", includedir_api+"types.h", api=api, profile=profile, binding=binding,
            platform_includes=[ type.moduleName for type in api.types if isinstance(type, Import) ],
            declarations=[ Template(declaration).render(binding=binding) for declaration in [ cls.getDeclaration(type) for type in api.types ] if len(declaration) > 0 ]
        )
        cls.render(template_engine, "types.inl", includedir_api+"types.inl", api=api, profile=profile, binding=binding,
            basic_enumerators=[ api.typeByIdentifier(binding.extensionType) ],
            generic_enumerators=[ api.typeByIdentifier(binding.enumType) ],
            bitfields=[ type for type in api.types if isinstance(type, BitfieldGroup) ]
        )
        cls.render(template_engine, "bitfield.h", includedir_api+"bitfield.h", api=api, profile=profile, binding=binding,
            groups=[ type for type in api.types if isinstance(type, BitfieldGroup) and len(type.values) > 0 ],
            constants=[ constant for constant in api.constants if len(constant.groups) > 0 and isinstance(constant.groups[0], BitfieldGroup) ],
            max_constant_length=str(max([ len(constant.identifier) for constant in api.constants if len(constant.groups) > 0 and isinstance(constant.groups[0], BitfieldGroup) ]))
        )
        cls.render(template_engine, "enum.h", includedir_api+"enum.h", api=api, profile=profile, binding=binding,
            groups=[ type for type in api.types if isinstance(type, Enumerator) and len(type.values) > 0 ],
            constants=[ constant for constant in api.constants if len(constant.groups) > 0 and isinstance(constant.groups[0], Enumerator) ],
            max_constant_length=str(max([ len(constant.identifier) for constant in api.constants if len(constant.groups) > 0 and isinstance(constant.groups[0], Enumerator) ]))
        )
        cls.render(template_engine, "functions.h", includedir_api+"functions.h", api=api, profile=profile, binding=binding,
            functions=[ function for function in api.functions ]
        )
        cls.render(template_engine, "entrypoint.h", includedir_api+"{{binding.baseNamespace}}.h", api=api, profile=profile, binding=binding)

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
            groups=[ type for type in api.types if isinstance(type, BitfieldGroup) and len(type.values) > 0 ]
        )
        cls.render(template_engine, "Meta_Maps.h", sourcedir_aux+"Meta_Maps.h", api=api, profile=profile, binding=binding,
            groups=[ type for type in api.types if isinstance(type, BitfieldGroup) and len(type.values) > 0 ]
        )
        cls.render(template_engine, "Meta_getStringByBitfield.cpp", sourcedir_aux+"Meta_getStringByBitfield.cpp", api=api, profile=profile, binding=binding,
            groups=[ type for type in api.types if isinstance(type, BitfieldGroup) and len(type.values) > 0 ]
        )
        cls.render(template_engine, "Meta_StringsByBitfield.cpp", sourcedir_aux+"Meta_StringsByBitfield.cpp", api=api, profile=profile, binding=binding,
            groups=[ type for type in api.types if isinstance(type, BitfieldGroup) and len(type.values) > 0 ]
        )
        cls.render(template_engine, "Meta_BitfieldsByString.cpp", sourcedir_aux+"Meta_BitfieldsByString.cpp", api=api, profile=profile, binding=binding,
            groups=cls.identifierPrefixGroups(api, [ constant for constant in api.constants if len(constant.groups) > 0 and isinstance(constant.groups[0], BitfieldGroup) ], len(profile.uppercasePrefix))
        )
        cls.render(template_engine, "Meta_StringsByBoolean.cpp", sourcedir_aux+"Meta_StringsByBoolean.cpp", api=api, profile=profile, binding=binding,
            booleans=[api.constantByIdentifier("GL_TRUE"), api.constantByIdentifier("GL_FALSE")]
        )
        cls.render(template_engine, "Meta_BooleansByString.cpp", sourcedir_aux+"Meta_BooleansByString.cpp", api=api, profile=profile, binding=binding,
            booleans=[api.constantByIdentifier("GL_TRUE"), api.constantByIdentifier("GL_FALSE")]
        )
        cls.render(template_engine, "Meta_StringsByEnum.cpp", sourcedir_aux+"Meta_StringsByEnum.cpp", api=api, profile=profile, binding=binding,
            constants=[ constant for constant in api.constants if len(constant.groups) > 0 and isinstance(constant.groups[0], Enumerator) ]
        )
        cls.render(template_engine, "Meta_EnumsByString.cpp", sourcedir_aux+"Meta_EnumsByString.cpp", api=api, profile=profile, binding=binding,
            groups=cls.identifierPrefixGroups(api, [ constant for constant in api.constants if len(constant.groups) > 0 and isinstance(constant.groups[0], Enumerator) ], len(profile.uppercasePrefix))
        )
        cls.render(template_engine, "Meta_StringsByExtension.cpp", sourcedir_aux+"Meta_StringsByExtension.cpp", api=api, profile=profile, binding=binding,
            extensions=api.extensions
        )
        cls.render(template_engine, "Meta_ExtensionsByString.cpp", sourcedir_aux+"Meta_ExtensionsByString.cpp", api=api, profile=profile, binding=binding,
            groups=cls.identifierPrefixGroups(api, api.extensions, len(profile.lowercasePrefix))
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

        cls.render(template_engine, "khrbinding-aux/RingBuffer.h", includedir_aux+"RingBuffer.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding-aux/RingBuffer.inl", includedir_aux+"RingBuffer.inl", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding-aux/types_to_string.h", includedir_aux+"types_to_string.h", api=api, profile=profile, binding=binding,
            enumerators=[ api.typeByIdentifier(binding.extensionType), api.typeByIdentifier(binding.enumType), api.typeByIdentifier(binding.booleanType) ],
            bitfields=[ type for type in api.types if isinstance(type, BitfieldGroup) ]
        )
        cls.render(template_engine, "khrbinding-aux/types_to_string.inl", includedir_aux+"types_to_string.inl", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding-aux/types_to_string.cpp", sourcedir_aux+"types_to_string.cpp", api=api, profile=profile, binding=binding,
            enumerators=[ api.typeByIdentifier(binding.extensionType), api.typeByIdentifier(binding.enumType), api.typeByIdentifier(binding.booleanType) ],
            bitfields=[ type for type in api.types if isinstance(type, BitfieldGroup) ],
            cStringTypes=[ "GLubyte", "GLchar" ],
            cPointerTypes=[ "GLvoid" ],
            types=[ type for type in api.types if not type.hideDeclaration ]
        )
        
        cls.render(template_engine, "khrbinding-aux/ValidVersions.h", includedir_aux+"ValidVersions.h", api=api, profile=profile, binding=binding)
        cls.render(template_engine, "khrbinding-aux/ValidVersions.cpp", sourcedir_aux+"ValidVersions.cpp", api=api, profile=profile, binding=binding)

        ## Generate function-related files with specific contexts for each initial letter of the function name
        #for functionGroup in generalContext["functionsByInitial"]["groups"]:
        #    specificContext = generalContext.copy()
        #    specificContext["currentFunctionGroup"] = functionGroup
        #    specificContext["currentFunctionInitial"] = functionGroup["name"].lower()

        #    Generator.generate(specificContext, pjoin(sourcedir_api, "functions_{currentFunctionInitial}.cpp"),
        #                       "functions.cpp")
        #    Generator.generate(specificContext, pjoin(sourcedir, "Binding_objects_{currentFunctionInitial}.cpp"),
        #                       "Binding_objects.cpp")

        ## Generate files with ApiMemberSet-specific contexts
        #for feature, core, ext in context.apiMemberSets():
        #    specificContext = context.apiMemberSetSpecific(feature, core, ext)

        #    Generator.generate(specificContext, pjoin(includedir_api, "boolean.h"), "booleanF.h")
        #    Generator.generate(specificContext, pjoin(includedir_api, "values.h"), "valuesF.h")
        #    Generator.generate(specificContext, pjoin(includedir_api, "types.h"), "typesF.h")
        #    Generator.generate(specificContext, pjoin(includedir_api, "bitfield.h"), "bitfieldF.h")
        #    Generator.generate(specificContext, pjoin(includedir_api, "enum.h"), "enumF.h")
        #    Generator.generate(specificContext, pjoin(includedir_api, "functions.h"), "functionsF.h")
        #    Generator.generate(specificContext, pjoin(includedir_api, "{api}.h"), "entrypointF.h")

    @classmethod
    def identifierPrefixGroups(cls, api, values, lookupOffset):
        result = { chr(alpha):[] for alpha in range(ord('A'), ord('Z')+1) }
        result["0"] = []
        for value in values:
            result[value.identifier[lookupOffset].upper() if value.identifier[lookupOffset].isalpha() else '0'].append(value)
        return result

    @classmethod
    def identifierPrefixGroupsDict(cls, api, dictionary, lookupOffset):
        result = { chr(alpha):{} for alpha in range(ord('A'), ord('Z')+1) }
        result["0"] = {}
        for key, values in dictionary.items():
            result[key.identifier[lookupOffset].upper() if key.identifier[lookupOffset].isalpha() else '0'][key] = values
        return result

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
        
        return ""
