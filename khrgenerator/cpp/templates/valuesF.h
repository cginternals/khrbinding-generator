
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>
#include <{{api.identifier}}binding/{{api.identifier}}/values.h>


namespace {{api.identifier}}{{memberSet}}
{


{{#valuesByType.groups}}
{{#items}}
using {{api.identifier}}::{{item.identifier}};
{{/items}}

{{/valuesByType.groups}}
{{#valuesByType.empty}}


{{/valuesByType.empty}}

} // namespace {{api.identifier}}{{memberSet}}
