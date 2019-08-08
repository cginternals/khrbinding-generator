
#pragma once


#include <{{api.identifer}}binding/no{{api.identifer}}.h>
#include <{{api.identifer}}binding/{{api.identifer}}/types.h>


namespace {{api.identifer}}{{memberSet}}
{


{% for type in types|sort(attribute='identifier') %}
using {{api.identifer}}::{{type.identifier}};
{% endfor %}


} // namespace {{api.identifer}}{{memberSet}}
