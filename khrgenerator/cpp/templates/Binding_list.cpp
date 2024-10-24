
#include "Binding_pch.h"


using namespace {{binding.baseNamespace}};


namespace {{binding.namespace}}
{


const Binding::array_t Binding::s_functions =
{{ "{{" }}
{%- for function in functions|sort(attribute='identifier') %}
    &{{function.namespaceLessIdentifier}}{{ "," if not loop.last }}
{%- endfor %}
{{ "}}" }};


} // namespace {{binding.namespace}}
