
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/enum.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


const std::unordered_map<{{profile.enumType}}, std::string> Meta_StringsByEnum =
{
{%- for constant in constants|sort(attribute='identifier') %}
    { {{profile.enumType}}::{{constant.identifier}}, "{{constant.identifier}}" }{% if not loop.last %},{% endif %}
{%- endfor %}
};


} } // namespace {{api.identifier}}binding::aux
