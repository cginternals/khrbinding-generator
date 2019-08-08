
#pragma once


#include <{{api.identifer}}binding/no{{api.identifer}}.h>

#include <{{api.identifer}}binding/{{api.identifer}}/enum.h>


namespace {{api.identifer}}{{memberSet}}
{


// import enums to namespace


{{#enumsByGroup.groups}}
// {{name}}

{{#items}}
{{#isPrimary}}
using {{api.identifer}}::{{item.identifier}};
{{/isPrimary}}
{{#isSecondary}}
// using {{api.identifer}}::{{item.identifier}}; // reuse {{item.primaryGroup}}
{{/isSecondary}}
{{/items}}

{{/enumsByGroup.groups}}


} // namespace {{api.identifer}}{{memberSet}}
