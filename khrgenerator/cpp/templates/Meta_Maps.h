
#pragma once


#include <string>
#include <map>
#include <unordered_map>
#include <vector>
#include <set>
#include <array>

#include <{{binding.identifier}}/{{binding.baseNamespace}}/types.h>
#include <{{binding.identifier}}/{{binding.baseNamespace}}/extension.h>


namespace {{binding.namespace}}
{


class Version;


namespace {{binding.auxNamespace}}
{


extern const std::array<std::unordered_map<std::string, {{binding.baseNamespace}}::{{binding.extensionType}}>, 27> Meta_ExtensionsByStringMaps;
extern const std::unordered_map<{{binding.baseNamespace}}::{{binding.extensionType}}, Version> Meta_ReqVersionsByExtension;

extern const std::unordered_map<{{binding.baseNamespace}}::{{binding.booleanType}}, std::string> Meta_StringsByBoolean;
extern const std::multimap<{{binding.baseNamespace}}::{{binding.enumType}}, std::string> Meta_StringsByEnum;
extern const std::unordered_map<{{binding.baseNamespace}}::{{binding.extensionType}}, std::string> Meta_StringsByExtension;
extern const std::unordered_map<{{binding.baseNamespace}}::{{binding.extensionType}}, std::set<std::string>> Meta_FunctionStringsByExtension;
extern const std::map<Version, std::set<std::string>> Meta_FunctionStringsByVersion;

{% for group in bitfieldGroups|sort(attribute='identifier') -%}
extern const std::unordered_map<{{binding.baseNamespace}}::{{group.identifier}}, std::string> Meta_StringsBy{{group.identifier}};
{% endfor %}
{% for group in enumGroups|sort(attribute='identifier') -%}
extern const std::unordered_map<{{binding.baseNamespace}}::{{group.identifier}}, std::string> Meta_StringsBy{{group.identifier}};
{% endfor %}
extern const std::array<std::unordered_map<std::string, {{binding.baseNamespace}}::{{binding.bitfieldType}}>, 27> Meta_BitfieldsByStringMaps;
extern const std::unordered_map<std::string, {{binding.baseNamespace}}::{{binding.booleanType}}> Meta_BooleansByString;
extern const std::array<std::unordered_map<std::string, {{binding.baseNamespace}}::{{binding.enumType}}>, 27> Meta_EnumsByStringMaps;
extern const std::array<std::unordered_map<std::string, std::set<{{binding.baseNamespace}}::{{binding.extensionType}}>>, 27> Meta_ExtensionsByFunctionStringMaps;


} } // namespace {{binding.bindingAuxNamespace}}
