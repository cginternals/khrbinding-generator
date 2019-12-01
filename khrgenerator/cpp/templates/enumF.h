
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>

#include <{{api.identifier}}binding/{{api.identifier}}/enum.h>


namespace {{api.identifier}}{{memberSet}}
{


// use enum type
using {{api.identifier}}::{{binding.enumType}};


// import enums to namespace
{%- for constant in constants|sort(attribute='identifier') %}
using {{api.identifier}}::{{constant.identifier}};
{%- endfor %}


} // namespace {{api.identifier}}{{memberSet}}
