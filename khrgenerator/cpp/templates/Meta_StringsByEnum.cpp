
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{api.identifier}}/enum.h>


using namespace {{api.identifier}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


const std::unordered_map<{{binding.enumType}}, std::string> Meta_StringsByEnum =
{
{%- for constant in constants|sort(attribute='identifier') %}
    { {{binding.enumType}}::{{constant.identifier}}, "{{constant.identifier}}" }{% if not loop.last %},{% endif %}
{%- endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
