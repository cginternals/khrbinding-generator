
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{binding.baseNamespace}}/enum.h>


using namespace {{binding.baseNamespace}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


const std::multimap<{{binding.enumType}}, std::string> Meta_StringsByEnum =
{
{%- for constant in constants|sort(attribute='identifier') %}
    { {{binding.enumType}}::{{constant.identifier}}, "{{constant.identifier}}" }{% if not loop.last %},{% endif %}
{%- endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
