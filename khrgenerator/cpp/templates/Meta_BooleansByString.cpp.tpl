
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/boolean.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


const std::unordered_map<std::string, {{profile.booleanType}}> Meta_BooleansByString =
{
{%- for boolean in booleans|sort(attribute='identifier') %}
    { "{{boolean.identifier}}", {{api.identifier}}::{{boolean.identifier}} }{% if not loop.last %},{% endif %}
{%- endfor %}
};


} } // namespace {{api.identifier}}binding::aux
