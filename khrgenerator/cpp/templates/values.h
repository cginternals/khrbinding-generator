
#pragma once


#include <{{binding.identifier}}/{{binding.identifier}}_features.h>

#include <{{binding.identifier}}/no{{binding.baseNamespace}}.h>
#include <{{binding.identifier}}/{{binding.baseNamespace}}/types.h>


namespace {{binding.baseNamespace}}
{


{% for constant in values.values|sort(attribute='identifier') -%}
{{binding.constexpr}} static const {{constant.type.identifier}} {{constant.identifier}} = {{constant.value}};
{% endfor %}

} // namespace {{binding.baseNamespace}}
