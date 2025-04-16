
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{binding.baseNamespace}}/bitfield.h>


using namespace {{binding.baseNamespace}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


{% for group in groups|sort(attribute='identifier') -%}
const std::unordered_map<{{group.identifier}}, std::string> Meta_StringsBy{{group.identifier}} =
{
{%- for value in group.values|sort(attribute='identifier') %}
    { {{group.identifier}}::{{value.identifier}}, "{{value.identifier}}" }{% if not loop.last %},{% endif %}
{%- endfor %}
};

{% endfor %}
} } // namespace {{binding.bindingAuxNamespace}}
