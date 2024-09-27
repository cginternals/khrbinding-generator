
#pragma once


#include <{{binding.identifier}}/no{{api.identifier}}.h>

#include <{{binding.identifier}}/{{api.identifier}}/bitfield.h>


namespace {{apiString}}{{memberSet}}
{


// import bitfields to namespace
{%- for constant in constants|sort(attribute='identifier') %}
using {{api.identifier}}::{{constant.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
