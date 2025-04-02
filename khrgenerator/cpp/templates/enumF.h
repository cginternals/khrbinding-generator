
#pragma once


#include <{{profile.bindingNamespace}}/no{{binding.baseNamespace}}.h>

#include <{{profile.bindingNamespace}}/{{binding.baseNamespace}}/enum.h>


namespace {{apiString}}{{memberSet}}
{


// use enum type
using {{binding.baseNamespace}}::{{binding.enumType}};


// import enums to namespace
{%- for constant in constants|sort(attribute='identifier') %}
using {{binding.baseNamespace}}::{{constant.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
