
#pragma once


#include <{{binding.identifer}}/no{{api.identifer}}.h>
#include <{{binding.identifer}}/{{api.identifer}}/functions.h>


namespace {{api.identifer}}{{memberSet}}
{

// import functions
{%- for function in functions %}
using {{api.identifer}}::{{function.identifier}};
{%- endfor %}

} // namespace {{api.identifer}}{{memberSet}}
