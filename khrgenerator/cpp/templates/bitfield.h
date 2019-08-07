
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>

#include <{{api.identifier}}binding/{{api.identifier}}binding_features.h>

#include <{{api.identifier}}binding/SharedBitfield.h>


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
{{api.identifier|upper}}BINDING_CONSTEXPR static const {{api.identifier}}binding::SharedBitfield<{% for group in constant.groups %}{{group.identifier}}{{ ", " if not loop.last }}{% endfor %}> {{constant.identifier}} = {{constant.groups[0].identifier}}::{{constant.identifier}};
{%- else -%}
{{api.identifier|upper}}BINDING_CONSTEXPR static const {{constant.groups[0].identifier}} {{constant.identifier}} = {{constant.groups[0].identifier}}::{{constant.identifier}};
{%- endif %}
{% endfor %}

} // namespace {{api.identifier}}
