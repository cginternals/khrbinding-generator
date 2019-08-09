
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>

#include <{{api.identifier}}binding/{{api.identifier}}/values.h>


namespace {{api.identifier}}{{memberSet}}
{


// import values to namespace
{%- for value in values|sort(attribute='identifier') %}
using {{api.identifier}}::{{value.identifier}};
{%- endfor %}


} // namespace {{api.identifier}}{{memberSet}}
