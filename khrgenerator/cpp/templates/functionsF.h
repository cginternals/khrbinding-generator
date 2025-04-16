
#pragma once


#include <{{binding.identifier}}/no{{binding.baseNamespace}}.h>
#include <{{binding.identifier}}/{{binding.baseNamespace}}/functions.h>


namespace {{apiString}}{{memberSet}}
{

// import functions
{%- for function in functions|sort(attribute='identifier') %}
using {{binding.baseNamespace}}::{{function.identifier}};
{%- endfor %}

} // namespace {{apiString}}{{memberSet}}
