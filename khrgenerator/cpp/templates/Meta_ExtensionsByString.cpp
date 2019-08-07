
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{api.identifier}}/extension.h>


using namespace {{api.identifier}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


{% for groupname, extensions in groups|dictsort -%}
{% if extensions|length == 0 -%}
const std::unordered_map<std::string, {{binding.extensionType}}> Meta_ExtensionsByString_{{groupname}}{};
{% else -%}
const std::unordered_map<std::string, {{binding.extensionType}}> Meta_ExtensionsByString_{{groupname}} =
{
{%- for extension in extensions %}
    { "{{extension.identifier}}", {{binding.extensionType}}::{{extension.identifier}} }{{ "," if not loop.last }}
{%- endfor %}
};
{% endif %}
{% endfor -%}
const std::array<std::unordered_map<std::string, {{api.identifier}}::{{binding.extensionType}}>, {{groups|length}}> Meta_ExtensionsByStringMaps =
{ {
{%- for groupname, extensions in groups|dictsort %}
    Meta_ExtensionsByString_{{groupname}}{{ "," if not loop.last }}
{%- endfor %}
} };


} } // namespace {{binding.bindingAuxNamespace}}
