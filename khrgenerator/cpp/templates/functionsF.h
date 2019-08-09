
#pragma once


#include <{{binding.identifier}}/no{{api.identifier}}.h>
#include <{{binding.identifier}}/{{api.identifier}}/functions.h>


namespace {{api.identifier}}{{memberSet}}
{

// import functions
{%- for function in functions|sort(attribute='identifier') %}
using {{api.identifier}}::{{function.identifier}};
{%- endfor %}

} // namespace {{api.identifier}}{{memberSet}}
