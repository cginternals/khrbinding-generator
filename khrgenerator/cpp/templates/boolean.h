
#pragma once


#include <{{api.identifer}}binding/no{{api.identifer}}.h>

#include <{{api.identifer}}binding/{{api.identifer}}binding_features.h>


namespace {{api.identifer}}
{


enum class GLboolean : unsigned char
{
{{#booleans.items}}
    {{item.identifier}} = {{item.value}}{{^last}},{{/last}}
{{/booleans.items}}
};

// import booleans to namespace

{{#booleans.items}}
{{ucapi}}BINDING_CONSTEXPR static const GLboolean {{item.identifier}} = GLboolean::{{item.identifier}};
{{/booleans.items}}


} // namespace {{api.identifer}}
