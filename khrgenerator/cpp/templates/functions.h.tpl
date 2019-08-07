
#pragma once


#include <{{api.identifier}}binding/{{api.identifier}}binding_api.h>

#include <{{api.identifier}}binding/no{{api.identifier}}.h>
#include <{{api.identifier}}binding/{{api.identifier}}/types.h>


namespace {{api.identifier}}
{


{% for function in functions|sort(attribute='identifier') -%}
{{api.identifier|upper}}BINDING_API {{function.returnType.identifier}} {{function.identifier}}({% for param in function.parameters %}{{ param.type.identifier }} {{ param.name }}{% if not loop.last %}, {% endif %}{% endfor %});
{% endfor %}

} // namespace {{api.identifier}}


// Include function patches due to dinstinguished types GLint, GLuint, GLenum, and GLboolean
#include <{{api.identifier}}binding/{{api.identifier}}/functions-patches.h>
