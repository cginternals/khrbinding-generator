
#pragma once


#include <{{binding.identifer}}/no{{api.identifer}}.h>
#include <{{binding.identifer}}/{{api.identifer}}/functions.h>


namespace {{api.identifer}}{{memberSet}}
{


{{#functions.items}}
using {{api.identifer}}::{{item.identifier}};
{{/functions.items}}


} // namespace {{api.identifer}}{{memberSet}}
