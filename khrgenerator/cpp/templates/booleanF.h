
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>

#include <{{api.identifier}}binding/{{api.identifier}}/boolean.h>


namespace {{api.identifier}}{{memberSet}}
{


// import booleans to namespace

{{#booleans.items}}
using {{api.identifier}}::{{item.identifier}};
{{/booleans.items}}


} // namespace {{api.identifier}}{{memberSet}}
