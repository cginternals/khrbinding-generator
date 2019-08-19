
#pragma once


#include <{{binding.identifier}}/{{nativeType}}.h>

#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>
#include <{{binding.identifier}}/no{{api.identifier}}.h>


namespace {{api.identifier}}
{


using {{binding.booleanType}} = {{binding.identifier}}::{{nativeType}};


// import booleans to namespace

{% for constant in values|sort(attribute='identifier') -%}
{{binding.constexpr}} static const {{binding.booleanType}} {{constant.identifier}} = {{binding.booleanType}}({{constant.value}});
{% endfor %}

} // namespace {{api.identifier}}
