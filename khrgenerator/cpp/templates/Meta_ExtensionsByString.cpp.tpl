
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/extension.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


{% for groupname, extensions in groups|dictsort -%}
{% if extensions|length == 0 -%}
const std::unordered_map<std::string, {{profile.extensionType}}> Meta_ExtensionsByString_{{groupname}}{};
{% else -%}
const std::unordered_map<std::string, {{profile.extensionType}}> Meta_ExtensionsByString_{{groupname}} =
{
{%- for extension in extensions %}
    { "{{extension.identifier}}", {{profile.extensionType}}::{{extension.identifier}} }{{ "," if not loop.last }}
{%- endfor %}
};
{% endif %}
{% endfor -%}
const std::array<std::unordered_map<std::string, {{api.identifier}}::{{profile.extensionType}}>, {{groups|length}}> Meta_ExtensionsByStringMaps =
{ {
{%- for groupname, extensions in groups|dictsort %}
    Meta_ExtensionsByString_{{groupname}}{{ "," if not loop.last }}
{%- endfor %}
} };


} } // namespace {{api.identifier}}binding::aux
