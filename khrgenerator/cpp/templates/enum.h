
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>

#include <{{api.identifier}}binding/{{api.identifier}}binding_features.h>


namespace {{api.identifier}}
{


enum class {{profile.enumType}} : unsigned int
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
{{api.identifier|upper}}BINDING_CONSTEXPR static const {{profile.enumType}} {{value.identifier}} = {{profile.enumType}}::{{value.identifier}};
{% else -%}
// {{api.identifier|upper}}BINDING_CONSTEXPR static const {{profile.enumType}} {{value.identifier}} = {{profile.enumType}}::{{value.identifier}}; // reuse {{value.groups[0].identifier}}
{% endif -%}
{% endfor -%}
{% endfor %}

} // namespace {{api.identifier}}
