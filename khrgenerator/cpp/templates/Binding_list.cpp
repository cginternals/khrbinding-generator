
#include "Binding_pch.h"


using namespace {{api.identifier}};


namespace {{binding.namespace}}
{


const Binding::array_t Binding::s_functions =
{{ "{{" }}
{%- for function in functions|sort(attribute='identifier') %}
    &{{function.identifier}}{{ "," if not loop.last }}
{%- endfor %}
{{ "}}" }};


} // namespace {{binding.namespace}}
