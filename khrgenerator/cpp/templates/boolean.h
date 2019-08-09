
#pragma once


#include <{{api.identifier}}binding/no{{api.identifier}}.h>

#include <{{api.identifier}}binding/{{api.identifier}}binding_features.h>


namespace {{api.identifier}}
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


} // namespace {{api.identifier}}
