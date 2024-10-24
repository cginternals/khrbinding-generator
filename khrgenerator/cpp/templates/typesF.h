
#pragma once


#include <{{binding.baseNamespace}}binding/no{{binding.baseNamespace}}.h>
#include <{{binding.baseNamespace}}binding/{{binding.baseNamespace}}/types.h>


namespace {{apiString}}{{memberSet}}
{


{% for type in types|sort(attribute='identifier') %}
using {{binding.baseNamespace}}::{{type.identifier}};
{%- endfor %}


} // namespace {{apiString}}{{memberSet}}
