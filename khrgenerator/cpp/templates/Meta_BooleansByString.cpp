
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{binding.baseNamespace}}/boolean.h>


using namespace {{binding.baseNamespace}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


const std::unordered_map<std::string, {{binding.booleanType}}> Meta_BooleansByString =
{
{%- for boolean in booleans|sort(attribute='identifier') %}
    { "{{boolean.identifier}}", {{binding.baseNamespace}}::{{boolean.identifier}} }{% if not loop.last %},{% endif %}
{%- endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
