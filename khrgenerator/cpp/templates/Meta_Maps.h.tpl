
#pragma once


#include <string>
#include <map>
#include <unordered_map>
#include <vector>
#include <set>
#include <array>

#include <{{api.identifier}}binding/{{api.identifier}}/types.h>
#include <{{api.identifier}}binding/{{api.identifier}}/extension.h>


namespace {{api.identifier}}binding
{


class Version;


namespace aux
{


extern const std::array<std::unordered_map<std::string, {{api.identifier}}::{{profile.extensionType}}>, 27> Meta_ExtensionsByStringMaps;
extern const std::unordered_map<{{api.identifier}}::{{profile.extensionType}}, Version> Meta_ReqVersionsByExtension;

extern const std::unordered_map<{{api.identifier}}::{{profile.booleanType}}, std::string> Meta_StringsByBoolean;
extern const std::unordered_map<{{api.identifier}}::{{profile.enumType}}, std::string> Meta_StringsByEnum;
extern const std::unordered_map<{{api.identifier}}::{{profile.extensionType}}, std::string> Meta_StringsByExtension;
extern const std::unordered_map<{{api.identifier}}::{{profile.extensionType}}, std::set<std::string>> Meta_FunctionStringsByExtension;
extern const std::map<Version, std::set<std::string>> Meta_FunctionStringsByVersion;

{% for group in groups|sort(attribute='identifier') -%}
extern const std::unordered_map<{{api.identifier}}::{{group.identifier}}, std::string> Meta_StringsBy{{group.identifier}};
{% endfor %}
extern const std::array<std::unordered_map<std::string, {{api.identifier}}::{{profile.bitfieldType}}>, 27> Meta_BitfieldsByStringMaps;
extern const std::unordered_map<std::string, {{api.identifier}}::{{profile.booleanType}}> Meta_BooleansByString;
extern const std::array<std::unordered_map<std::string, {{api.identifier}}::{{profile.enumType}}>, 27> Meta_EnumsByStringMaps;
extern const std::array<std::unordered_map<std::string, std::set<{{api.identifier}}::{{profile.extensionType}}>>, 27> Meta_ExtensionsByFunctionStringMaps;


} } // namespace {{api.identifier}}binding::aux
