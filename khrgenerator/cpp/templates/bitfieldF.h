
#pragma once


#include <{{binding.identifer}}/no{{api.identifer}}.h>

#include <{{binding.identifer}}/{{api.identifer}}/bitfield.h>


namespace {{api.identifer}}{{memberSet}}
{


// import bitfields to namespace
{%- for constant in constants %}
using {{api.identifer}}::{{constant.identifier}};
{%- endfor %}


} // namespace {{api.identifer}}{{memberSet}}
