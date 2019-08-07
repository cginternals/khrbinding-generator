
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/extension.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


{% for groupname, functions in extensionsByFunction|dictsort -%}
{% if functions|length == 0 -%}
const std::unordered_map<std::string, std::set<{{profile.extensionType}}>> Meta_ExtensionsByFunctionString_{{groupname}}{};
{% else -%}
const std::unordered_map<std::string, std::set<{{profile.extensionType}}>> Meta_ExtensionsByFunctionString_{{groupname}} =
{
{%- for function, extensions in functions|dictsort %}{% if extensions|length > 0 %}
    { "{{function.identifier}}", { {% for extension in extensions|sort(attribute='identifier') %}{{profile.extensionType}}::{{extension.identifier}}{{", " if not loop.last}}{% endfor %} } }{{"," if not loop.last}}
{%- endif %}{% endfor %}
};
{% endif %}
{% endfor %}
const std::array<std::unordered_map<std::string, std::set<{{api.identifier}}::{{profile.extensionType}}>>, {{extensionsByFunction|length}}> Meta_ExtensionsByFunctionStringMaps =
{ {
{%- for groupname, function in extensionsByFunction|dictsort %}
    Meta_ExtensionsByFunctionString_{{groupname}}{{ "," if not loop.last }}
{%- endfor %}
} };


} } // namespace {{api.identifier}}binding::aux
