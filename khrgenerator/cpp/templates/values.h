
#pragma once


#include <{{api.identifier}}binding/{{api.identifier}}binding_features.h>

#include <{{api.identifier}}binding/no{{api.identifier}}.h>
#include <{{api.identifier}}binding/{{api.identifier}}/types.h>


namespace {{api.identifier}}
{


{% for constant in values.values -%}
{{api.identifier|upper}}BINDING_CONSTEXPR static const {{constant.type.identifier}} {{constant.identifier}} = {{constant.value}};
{% endfor %}

} // namespace {{api.identifier}}
