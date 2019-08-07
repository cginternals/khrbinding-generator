
#pragma once


#include <{{binding.identifier}}/no{{api.identifier}}.h>
#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>
#include <{{binding.identifier}}/{{api.identifier}}/boolean.h>

#include <cstddef>
#include <cstdint>
#include <array>
#include <string>

{% for include in binding.platformIncludes -%}
#include <{{include}}>
{% endfor %}
#ifdef _MSC_VER
#define {{api.identifier|upper}}_APIENTRY __stdcall
#else
#define {{api.identifier|upper}}_APIENTRY
#endif


namespace {{api.identifier}}
{

{{binding.additionalTypes}}
{% for type in types %}
{{type.definition}}
{% endfor %}

} // namespace {{api}}


// Type Integrations

{{#types.items}}
{{#item.integrations.hashable}}
{{#item}}{{>partials/types_hashable.h}}{{/item}}

{{/item.integrations.hashable}}
{{#item.integrations.addable}}
{{#item}}{{>partials/types_addable.h}}{{/item}}

{{/item.integrations.addable}}
{{#item.integrations.bitOperatable}}
{{#item}}{{>partials/types_bitOperatable.h}}{{/item}}

{{/item.integrations.bitOperatable}}
{{#item.integrations.comparable}}
{{#item}}{{>partials/types_comparable.h}}{{/item}}

{{/item.integrations.comparable}}
{{/types.items}}
