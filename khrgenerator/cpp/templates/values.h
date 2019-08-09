
#pragma once


#include <{{binding.identifier}}/{{binding.identifier}}_features.h>

#include <{{binding.identifier}}/no{{api.identifier}}.h>
#include <{{binding.identifier}}/{{api.identifier}}/types.h>


namespace {{api.identifier}}
{


{% for constant in values.values|sort(attribute='identifier') -%}
{{binding.constexpr}} static const {{constant.type.identifier}} {{constant.identifier}} = {{constant.value}};
{% endfor %}

} // namespace {{api.identifier}}
