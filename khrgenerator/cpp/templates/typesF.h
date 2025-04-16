
#pragma once


#include <{{profile.bindingNamespace}}/no{{binding.baseNamespace}}.h>
#include <{{profile.bindingNamespace}}/{{binding.baseNamespace}}/types.h>


namespace {{apiString}}{{memberSet}}
{


{% for type in types|sort(attribute='identifier') %}
using {{binding.baseNamespace}}::{{type.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
