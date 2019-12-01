
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>

#include <{{api.identifier}}binding/{{api.identifier}}/boolean.h>


namespace {{api.identifier}}{{memberSet}}
{


// use boolean type
using {{api.identifier}}::{{binding.booleanType}};


// import booleans to namespace
{%- for constant in constants|sort(attribute='identifier') %}
using {{api.identifier}}::{{constant.identifier}};
{%- endfor %}


} // namespace {{api.identifier}}{{memberSet}}
