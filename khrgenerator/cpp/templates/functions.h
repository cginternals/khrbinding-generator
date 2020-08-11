
#pragma once


#include <{{binding.identifier}}/{{binding.identifier}}_api.h>

#include <{{binding.identifier}}/no{{api.identifier}}.h>
#include <{{binding.identifier}}/{{api.identifier}}/types.h>


namespace {{api.identifier}}
{


{% for function in functions|sort(attribute='identifier') -%}
{{binding.apiExport}} {{function.returnType.identifier}} {{function.identifier}}({% for param in function.parameters %}{{ param.type.identifier }} {{ param.name }}{% if not loop.last %}, {% endif %}{% endfor %}) {{profile.noexceptMacro}};
{% endfor %}

} // namespace {{api.identifier}}


// Include function patches due to dinstinguished types GLint, GLuint, GLenum, and GLboolean
#include <{{binding.identifier}}/{{api.identifier}}/functions-patches.h>
