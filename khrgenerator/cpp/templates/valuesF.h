
#pragma once


#include <{{profile.bindingNamespace}}/no{{binding.baseNamespace}}.h>

#include <{{profile.bindingNamespace}}/{{binding.baseNamespace}}/values.h>


namespace {{apiString}}{{memberSet}}
{


// import values to namespace
{%- for value in values|sort(attribute='identifier') %}
using {{binding.baseNamespace}}::{{value.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
