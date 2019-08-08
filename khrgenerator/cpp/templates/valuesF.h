
#pragma once


#include <{{api.identifer}}binding/no{{api.identifer}}.h>
#include <{{api.identifer}}binding/{{api.identifer}}/values.h>


namespace {{api.identifer}}{{memberSet}}
{


{{#valuesByType.groups}}
{{#items}}
using {{api.identifer}}::{{item.identifier}};
{{/items}}

{{/valuesByType.groups}}
{{#valuesByType.empty}}


{{/valuesByType.empty}}

} // namespace {{api.identifer}}{{memberSet}}
