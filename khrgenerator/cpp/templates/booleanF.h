
#pragma once


#include <{{profile.bindingNamespace}}/no{{binding.baseNamespace}}.h>

#include <{{profile.bindingNamespace}}/{{binding.baseNamespace}}/boolean.h>


namespace {{apiString}}{{memberSet}}
{


// use boolean type
using {{binding.baseNamespace}}::{{binding.booleanType}};


// import booleans to namespace
{%- for constant in constants|sort(attribute='identifier') %}
using {{binding.baseNamespace}}::{{constant.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
