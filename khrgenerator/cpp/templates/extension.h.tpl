
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>


namespace {{api.identifier}}
{


enum class {{profile.extensionType}} : int // {{profile.extensionType}} is not a type introduced by {{api.identifier | upper}} API so far
{
    UNKNOWN = -1,
    {% for extension in api.extensions|sort(attribute='identifier') -%}
    {{extension.identifier}}{{ "," if not loop.last }}
    {% endfor %}
};


} // namespace {{api.identifier}}
