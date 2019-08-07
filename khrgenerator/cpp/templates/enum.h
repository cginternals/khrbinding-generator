
#pragma once


#include <{{binding.identifier}}/no{{api.identifier}}.h>

#include <{{binding.identifier}}/{{binding.identifier}}_features.h>


namespace {{api.identifier}}
{


enum class {{binding.enumType}} : unsigned int
{
{%- for group in groups|sort(attribute='identifier') %}
    // {{ group.identifier }}
{% for value in group.values|sort(attribute='value') -%}
{%- if group.identifier == value.groups[0].identifier %}
    {{ ("{:"+max_constant_length+"}").format(value.identifier) }} = {{value.value}},
{%- else %}
//  {{ ("{:"+max_constant_length+"}").format(value.identifier) }} = {{value.value}}, // reuse {{value.groups[0].identifier}}
{%- endif %}
{%- endfor %}
{% endfor %}
};


// import enums to namespace

{% for group in groups|sort(attribute='identifier') -%}
// {{ group.identifier }}

{% for value in group.values|sort(attribute='value') -%}
{% if group.identifier == value.groups[0].identifier -%}
{{binding.constexpr}} static const {{binding.enumType}} {{value.identifier}} = {{binding.enumType}}::{{value.identifier}};
{% else -%}
// {{binding.constexpr}} static const {{binding.enumType}} {{value.identifier}} = {{binding.enumType}}::{{value.identifier}}; // reuse {{value.groups[0].identifier}}
{% endif -%}
{% endfor -%}
{% endfor %}

} // namespace {{api.identifier}}
