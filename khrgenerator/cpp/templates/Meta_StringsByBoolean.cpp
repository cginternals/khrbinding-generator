
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{binding.baseNamespace}}/boolean.h>


using namespace {{binding.baseNamespace}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


const std::unordered_map<{{binding.booleanType}}, std::string> Meta_StringsByBoolean =
{
{%- for boolean in booleans|sort(attribute='identifier') %}
    { {{binding.baseNamespace}}::{{boolean.identifier}}, "{{boolean.identifier}}" }{% if not loop.last %},{% endif %}
{%- endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
