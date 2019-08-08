
#pragma once


#include <{{api.identifer}}binding/no{{api.identifer}}.h>
#include <{{api.identifer}}binding/{{api.identifer}}/functions.h>


namespace {{api.identifer}}{{memberSet}}
{


{{#functions.items}}
using {{api.identifer}}::{{item.identifier}};
{{/functions.items}}


} // namespace {{api.identifer}}{{memberSet}}
