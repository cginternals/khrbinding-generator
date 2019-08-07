
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/boolean.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


const std::unordered_map<{{profile.booleanType}}, std::string> Meta_StringsByBoolean =
{
{%- for boolean in booleans|sort(attribute='identifier') %}
    { {{api.identifier}}::{{boolean.identifier}}, "{{boolean.identifier}}" }{% if not loop.last %},{% endif %}
{%- endfor %}
};


} } // namespace {{api.identifier}}binding::aux
