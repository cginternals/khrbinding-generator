
#pragma once


#include <{{binding.identifier}}/no{{api.identifier}}.h>


namespace {{api.identifier}}
{


enum class {{binding.extensionType}} : int // {{binding.extensionType}} is not a type introduced by {{api.identifier | upper}} API so far
{
    UNKNOWN = -1,
    {% for extension in api.extensions|sort(attribute='identifier') -%}
    {{extension.identifier}}{{ "," if not loop.last }}
    {% endfor %}
};


} // namespace {{api.identifier}}
