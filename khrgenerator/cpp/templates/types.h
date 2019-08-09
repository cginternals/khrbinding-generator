
#pragma once


#include <cstddef>
#include <cstdint>
#include <array>
#include <string>

{% for include in platform_includes -%}
#include <{{include}}>
{% endfor %}
#ifdef _MSC_VER
#define {{binding.apientry}} __stdcall
#else
#define {{binding.apientry}}
#endif

#include <{{binding.identifier}}/no{{api.identifier}}.h>
#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>
#include <{{binding.identifier}}/{{api.identifier}}/boolean.h>


namespace {{api.identifier}}
{

{{binding.additionalTypes}}
{% for declaration in declarations %}
{{declaration}}
{%- endfor %}

} // namespace {{api.identifier}}


#include <{{binding.identifier}}/{{api.identifier}}/types.inl>
