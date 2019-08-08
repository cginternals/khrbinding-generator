
#pragma once


#include <{{api.identifer}}binding/no{{api.identifer}}.h>

#include <{{api.identifer}}binding/{{api.identifer}}/boolean.h>


namespace {{api.identifer}}{{memberSet}}
{


// import booleans to namespace

{{#booleans.items}}
using {{api.identifer}}::{{item.identifier}};
{{/booleans.items}}


} // namespace {{api.identifer}}{{memberSet}}
