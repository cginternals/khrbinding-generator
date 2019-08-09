
#include "../Binding_pch.h"

#include <{{binding.identifier}}/{{api.identifier}}/functions.h>


namespace {{api.identifier}}
{

{% for function in functions|sort(attribute='identifier') %}
{{function.returnType.identifier}} {{function.identifier}}({% for parameter in function.parameters %}{{parameter.type.identifier}} {{parameter.name}}{{ ", " if not loop.last }}{% endfor %})
{
    return {{binding.namespace}}::Binding::{{function.namespaceLessIdentifier}}({% for parameter in function.parameters %}{{parameter.name}}{{ ", " if not loop.last }}{% endfor %});
}
{% endfor %}

} // namespace {{api.identifier}}
