
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{api.identifier}}/bitfield.h>


using namespace {{api.identifier}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{

{% for groupname, constants in groups|dictsort -%}
{% if constants|length == 0 %}
const std::unordered_map<std::string, {{binding.bitfieldType}}> Meta_BitfieldsByString_{{groupname}}{};
{%- else %}
const std::unordered_map<std::string, {{binding.bitfieldType}}> Meta_BitfieldsByString_{{groupname}} =
{
{%- for constant in constants|sort(attribute='identifier') %}
    { "{{constant.identifier}}", static_cast<{{binding.bitfieldType}}>({{constant.groups[0].identifier}}::{{constant.identifier}}) }{% if not loop.last %},{% endif %}
{%- endfor %}
};
{%- endif %}
{% endfor %}
const std::array<std::unordered_map<std::string, {{api.identifier}}::{{binding.bitfieldType}}>, {{groups|length}}> Meta_BitfieldsByStringMaps =
{ {
{%- for groupname, constants in groups|dictsort %}
    Meta_BitfieldsByString_{{groupname}}{% if not loop.last %},{% endif %}
{%- endfor %}
} };


} } // namespace {{binding.bindingAuxNamespace}}
