
#pragma once


#include <{{api.identifer}}binding/no{{api.identifer}}.h>

#include <{{api.identifer}}binding/{{api.identifer}}/bitfield.h>


namespace {{api.identifer}}{{memberSet}}
{


// import bitfields to namespace
{{#bitfields.multipleItems}}{{#bitfields.items}}using {{api.identifer}}::{{item.identifier}};
{{/bitfields.items}}{{/bitfields.multipleItems}}{{! test for multiple items to avoid using GL_NONE_BIT alone}}


} // namespace {{api.identifer}}{{memberSet}}
