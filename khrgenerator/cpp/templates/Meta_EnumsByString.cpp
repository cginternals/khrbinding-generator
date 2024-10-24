
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{binding.baseNamespace}}/enum.h>


using namespace {{binding.baseNamespace}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{

{% for groupname, constants in groups|dictsort -%}
{% if constants|length == 0 %}
const std::unordered_map<std::string, {{binding.enumType}}> Meta_EnumsByString_{{groupname}}{};
{%- else %}
const std::unordered_map<std::string, {{binding.enumType}}> Meta_EnumsByString_{{groupname}} =
{
{%- for constant in constants|sort(attribute='identifier') %}
    { "{{constant.identifier}}", {{binding.enumType}}::{{constant.identifier}} }{% if not loop.last %},{% endif %}
{%- endfor %}
};
{%- endif %}
{% endfor %}
const std::array<std::unordered_map<std::string, {{binding.baseNamespace}}::{{binding.enumType}}>, {{groups|length}}> Meta_EnumsByStringMaps =
{ {
{%- for groupname, constants in groups|dictsort %}
    Meta_EnumsByString_{{groupname}}{% if not loop.last %},{% endif %}
{%- endfor %}
} };


} } // namespace {{binding.bindingAuxNamespace}}
