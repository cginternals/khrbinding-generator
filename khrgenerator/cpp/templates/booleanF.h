
#pragma once


#include <{{binding.baseNamespace}}binding/no{{binding.baseNamespace}}.h>

#include <{{binding.baseNamespace}}binding/{{binding.baseNamespace}}/boolean.h>


namespace {{apiString}}{{memberSet}}
{


// use boolean type
using {{binding.baseNamespace}}::{{binding.booleanType}};


// import booleans to namespace
{%- for constant in constants|sort(attribute='identifier') %}
using {{binding.baseNamespace}}::{{constant.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
