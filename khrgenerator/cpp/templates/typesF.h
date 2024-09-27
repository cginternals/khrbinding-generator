
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>
#include <{{api.identifier}}binding/{{api.identifier}}/types.h>


namespace {{apiString}}{{memberSet}}
{


{% for type in types|sort(attribute='identifier') %}
using {{api.identifier}}::{{type.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
