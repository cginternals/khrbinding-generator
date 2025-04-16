
#pragma once


#include <{{binding.identifier}}/no{{binding.baseNamespace}}.h>

#include <{{binding.identifier}}/{{binding.baseNamespace}}/bitfield.h>


namespace {{apiString}}{{memberSet}}
{


// import bitfields to namespace
{%- for constant in constants|sort(attribute='identifier') %}
using {{binding.baseNamespace}}::{{constant.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
