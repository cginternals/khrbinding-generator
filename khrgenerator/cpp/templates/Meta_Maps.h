
#pragma once


#include <string>
#include <map>
#include <unordered_map>
#include <vector>
#include <set>
#include <array>

#include <{{binding.identifier}}/{{api.identifier}}/types.h>
#include <{{binding.identifier}}/{{api.identifier}}/extension.h>


namespace {{binding.namespace}}
{


class Version;


namespace {{binding.auxNamespace}}
{


extern const std::array<std::unordered_map<std::string, {{api.identifier}}::{{binding.extensionType}}>, 27> Meta_ExtensionsByStringMaps;
extern const std::unordered_map<{{api.identifier}}::{{binding.extensionType}}, Version> Meta_ReqVersionsByExtension;

extern const std::unordered_map<{{api.identifier}}::{{binding.booleanType}}, std::string> Meta_StringsByBoolean;
extern const std::unordered_map<{{api.identifier}}::{{binding.enumType}}, std::string> Meta_StringsByEnum;
extern const std::unordered_map<{{api.identifier}}::{{binding.extensionType}}, std::string> Meta_StringsByExtension;
extern const std::unordered_map<{{api.identifier}}::{{binding.extensionType}}, std::set<std::string>> Meta_FunctionStringsByExtension;
extern const std::map<Version, std::set<std::string>> Meta_FunctionStringsByVersion;

{% for group in groups|sort(attribute='identifier') -%}
extern const std::unordered_map<{{api.identifier}}::{{group.identifier}}, std::string> Meta_StringsBy{{group.identifier}};
{% endfor %}
extern const std::array<std::unordered_map<std::string, {{api.identifier}}::{{binding.bitfieldType}}>, 27> Meta_BitfieldsByStringMaps;
extern const std::unordered_map<std::string, {{api.identifier}}::{{binding.booleanType}}> Meta_BooleansByString;
extern const std::array<std::unordered_map<std::string, {{api.identifier}}::{{binding.enumType}}>, 27> Meta_EnumsByStringMaps;
extern const std::array<std::unordered_map<std::string, std::set<{{api.identifier}}::{{binding.extensionType}}>>, 27> Meta_ExtensionsByFunctionStringMaps;


} } // namespace {{binding.bindingAuxNamespace}}
