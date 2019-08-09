
#pragma once


#include <{{binding.identifier}}/no{{api.identifier}}.h>

#include <{{binding.identifier}}/{{api.identifier}}/bitfield.h>


namespace {{api.identifier}}{{memberSet}}
{


// import bitfields to namespace
{%- for constant in constants|sort(attribute='identifier') %}
using {{api.identifier}}::{{constant.identifier}};
{%- endfor %}


} // namespace {{api.identifier}}{{memberSet}}
