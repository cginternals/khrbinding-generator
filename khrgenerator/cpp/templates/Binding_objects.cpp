
#include "Binding_pch.h"


using namespace {{binding.baseNamespace}};


namespace {{binding.namespace}}
{

{% for function in functions|sort(attribute='identifier') %}
Function<{{function.returnType.identifier}}{{ ", " if function.parameters|length > 0 }}{% for parameter in function.parameters %}{{parameter.type.identifier}}{{ ", " if not loop.last }}{% endfor %}> Binding::{{function.namespaceLessIdentifier}}("{{function.identifier}}");
{%- endfor %}


} // namespace {{binding.namespace}}
