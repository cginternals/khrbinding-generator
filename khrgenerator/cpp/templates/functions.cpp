
#include "../Binding_pch.h"

#include <{{api.identifer}}binding/{{api.identifer}}/functions.h>


using namespace {{api.identifer}}binding;


namespace {{api.identifer}}
{


{{#currentFunctionGroup.items}}{{#item}}{{>partials/general_type}} {{identifier}}({{>partials/general_params}})
{
    return Binding::{{identifierNoGl}}({{#params.items}}{{item.name}}{{^last}}, {{/last}}{{/params.items}});
}

{{/item}}{{/currentFunctionGroup.items}}


} // namespace {{api.identifer}}
