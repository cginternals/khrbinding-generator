
#pragma once


#include <{{binding.identifier}}/no{{binding.baseNamespace}}.h>

#include <{{binding.identifier}}/{{binding.identifier}}_features.h>

#include <{{binding.identifier}}/SharedBitfield.h>


namespace {{binding.baseNamespace}}
{


{% for group in groups|sort(attribute="identifier") -%}
enum class {{group.identifier}} : unsigned int
{
{%- for value in group.values|sort(attribute="decimalValue") %}
    {%- set sorted_groups = value.groups|sort(attribute='identifier') %}
    {{ ("{:"+max_constant_length+"}").format(value.identifier) }} = {{value.value}}{{ "," if not loop.last }}{% if value.generic %} // Generic {{ value.identifier }}{% else %}{% if group.identifier != sorted_groups[0].identifier %} // reuse from {{ sorted_groups[0].identifier }}{% endif %}{% endif %}
{%- endfor %}
};


{% endfor -%}

// import bitfields to namespace

{% for constant in constants|sort(attribute="identifier") -%}
{%- set sorted_groups = constant.groups|sort(attribute='identifier') -%}
{% if sorted_groups|length > 1 -%}
{{binding.constexpr}} static const {{binding.identifier}}::SharedBitfield<{% for group in sorted_groups %}{{group.identifier}}{{ ", " if not loop.last }}{% endfor %}> {{constant.identifier}} = {{sorted_groups[0].identifier}}::{{constant.identifier}};
{%- else -%}
{{binding.constexpr}} static const {{sorted_groups[0].identifier}} {{constant.identifier}} = {{sorted_groups[0].identifier}}::{{constant.identifier}};
{%- endif %}
{% endfor %}

} // namespace {{binding.baseNamespace}}
