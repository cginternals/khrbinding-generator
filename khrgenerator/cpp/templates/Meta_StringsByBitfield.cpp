
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/bitfield.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


{% for group in groups|sort(attribute='identifier') -%}
const std::unordered_map<{{group.identifier}}, std::string> Meta_StringsBy{{group.identifier}} =
{
{%- for value in group.values|sort(attribute='identifier') %}
    { {{group.identifier}}::{{value.identifier}}, "{{value.identifier}}" }{% if not loop.last %},{% endif %}
{%- endfor %}
};

{% endfor %}
} } // namespace {{api.identifier}}binding::aux
