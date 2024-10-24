
#pragma once


#include <{{binding.identifier}}/no{{binding.baseNamespace}}.h>

#include <{{binding.identifier}}/{{binding.identifier}}_features.h>


namespace {{binding.baseNamespace}}
{


enum class {{binding.enumType}} : unsigned int
{
{%- for group in groups|sort(attribute='identifier') %}
    // {{ group.identifier }}
{% for value in group.values|sort(attribute='value') -%}
{%- set sorted_groups = value.groups|rejectattr("identifier", "equalto", binding.enumType)|sort(attribute='identifier') -%}
{%- if group.identifier == sorted_groups[0].identifier %}
    {{ ("{:"+max_constant_length+"}").format(value.identifier) }} = {{value.value}},
{%- else %}
//  {{ ("{:"+max_constant_length+"}").format(value.identifier) }} = {{value.value}}, // reuse {{sorted_groups[0].identifier}}
{%- endif %}
{%- endfor %}
{% endfor %}
};


// import enums to namespace

{% for group in groups|sort(attribute='identifier') -%}
// {{ group.identifier }}

{% for value in group.values|sort(attribute='value') -%}
{%- set sorted_groups = value.groups|rejectattr("identifier", "equalto", binding.enumType)|sort(attribute='identifier') -%}
{% if group.identifier == sorted_groups[0].identifier -%}
{{binding.constexpr}} static const {{binding.enumType}} {{value.identifier}} = {{binding.enumType}}::{{value.identifier}};
{% else -%}
// {{binding.constexpr}} static const {{binding.enumType}} {{value.identifier}} = {{binding.enumType}}::{{value.identifier}}; // reuse {{sorted_groups[0].identifier}}
{% endif -%}
{% endfor %}
{% endfor %}

} // namespace {{binding.baseNamespace}}
