
#pragma once


#include <{{binding.identifier}}/no{{api.identifier}}.h>

#include <{{binding.identifier}}/{{binding.identifier}}_features.h>

#include <{{binding.identifier}}/SharedBitfield.h>


namespace {{api.identifier}}
{


{% for group in groups|sort(attribute="identifier") -%}
enum class {{group.identifier}} : unsigned int
{
{%- for value in group.values|sort(attribute="value") %}
    {{ ("{:"+max_constant_length+"}").format(value.identifier) }} = {{value.value}}{{ "," if not loop.last }}{% if value.generic %} // Generic {{ value.identifier }}{% else %}{% if group.identifier != value.groups[0].identifier %} // reuse from {{ value.groups[0].identifier }}{% endif %}{% endif %}
{%- endfor %}
};


{% endfor -%}

// import bitfields to namespace

{% for constant in constants|sort(attribute="identifier") -%}
{% if constant.groups|length > 1 -%}
{{binding.constexpr}} static const {{binding.identifier}}::SharedBitfield<{% for group in constant.groups %}{{group.identifier}}{{ ", " if not loop.last }}{% endfor %}> {{constant.identifier}} = {{constant.groups[0].identifier}}::{{constant.identifier}};
{%- else -%}
{{binding.constexpr}} static const {{constant.groups[0].identifier}} {{constant.identifier}} = {{constant.groups[0].identifier}}::{{constant.identifier}};
{%- endif %}
{% endfor %}

} // namespace {{api.identifier}}
