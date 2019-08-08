
#pragma once


#include <{{api.identifer}}binding/no{{api.identifer}}.h>
#include <{{api.identifer}}binding/{{api.identifer}}/types.h>


namespace {{api.identifer}}{{memberSet}}
{


{{#types.items}}
using {{api.identifer}}::{{item.identifier}};
{{/types.items}}


} // namespace {{api.identifer}}{{memberSet}}
