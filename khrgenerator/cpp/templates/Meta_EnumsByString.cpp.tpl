
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/enum.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{

{% for groupname, constants in groups|dictsort -%}
{% if constants|length == 0 %}
const std::unordered_map<std::string, {{profile.enumType}}> Meta_EnumsByString_{{groupname}}{};
{%- else %}
const std::unordered_map<std::string, {{profile.enumType}}> Meta_EnumsByString_{{groupname}} =
{
{%- for constant in constants|sort(attribute='identifier') %}
    { "{{constant.identifier}}", static_cast<{{profile.enumType}}>({{constant.groups[0].identifier}}::{{constant.identifier}}) }{% if not loop.last %},{% endif %}
{%- endfor %}
};
{%- endif %}
{% endfor %}
const std::array<std::unordered_map<std::string, {{api.identifier}}::{{profile.enumType}}>, {{groups|length}}> Meta_EnumsByStringMaps =
{ {
{%- for groupname, constants in groups|dictsort %}
    Meta_EnumsByString_{{groupname}}{% if not loop.last %},{% endif %}
{%- endfor %}
} };


} } // namespace {{api.identifier}}binding::aux
