
#pragma once


#include <{{binding.baseNamespace}}binding/no{{binding.baseNamespace}}.h>

#include <{{binding.baseNamespace}}binding/{{binding.baseNamespace}}/values.h>


namespace {{apiString}}{{memberSet}}
{


// import values to namespace
{%- for value in values|sort(attribute='identifier') %}
using {{binding.baseNamespace}}::{{value.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
