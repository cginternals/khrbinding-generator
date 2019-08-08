
#pragma once


#include <{{api.identifer}}binding/no{{api.identifer}}.h>

#include <{{api.identifer}}binding/{{api.identifer}}/enum.h>


namespace {{api.identifer}}{{memberSet}}
{


// import enums to namespace
{%- for constant in constants %}
using {{api.identifer}}::{{constant.identifier}};
{%- endfor %}

} // namespace {{api.identifer}}{{memberSet}}
