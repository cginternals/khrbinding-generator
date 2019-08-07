
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{api.identifier}}/boolean.h>


using namespace {{api.identifier}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


const std::unordered_map<std::string, {{binding.booleanType}}> Meta_BooleansByString =
{
{%- for boolean in booleans|sort(attribute='identifier') %}
    { "{{boolean.identifier}}", {{api.identifier}}::{{boolean.identifier}} }{% if not loop.last %},{% endif %}
{%- endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
