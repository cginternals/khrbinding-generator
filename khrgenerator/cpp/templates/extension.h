
#pragma once


#include <{{binding.identifier}}/no{{binding.baseNamespace}}.h>


namespace {{binding.baseNamespace}}
{


enum class {{binding.extensionType}} : int // {{binding.extensionType}} is not a type introduced by {{binding.baseNamespace | upper}} API so far
{
    UNKNOWN = -1,
    {% for extension in api.extensions|sort(attribute='identifier') -%}
    {{extension.identifier}}{{ "," if not loop.last }}
    {% endfor %}
};


} // namespace {{binding.baseNamespace}}
