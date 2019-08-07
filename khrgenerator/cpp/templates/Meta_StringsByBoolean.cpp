
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{api.identifier}}/boolean.h>


using namespace {{api.identifier}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


const std::unordered_map<{{binding.booleanType}}, std::string> Meta_StringsByBoolean =
{
{%- for boolean in booleans|sort(attribute='identifier') %}
    { {{api.identifier}}::{{boolean.identifier}}, "{{boolean.identifier}}" }{% if not loop.last %},{% endif %}
{%- endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
