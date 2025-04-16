
#pragma once


#include <{{binding.identifier}}/{{binding.identifier}}_api.h>

#include <{{binding.identifier}}/no{{binding.baseNamespace}}.h>
#include <{{binding.identifier}}/{{binding.baseNamespace}}/types.h>


namespace {{binding.baseNamespace}}
{


{% for function in functions|sort(attribute='identifier') -%}
{{binding.apiExport}} {{function.returnType.identifier}} {{function.identifier}}({% for param in function.parameters %}{{ param.type.identifier }} {{ param.name }}{% if not loop.last %}, {% endif %}{% endfor %});
{% endfor %}

} // namespace {{binding.baseNamespace}}


// Include function patches due to dinstinguished types GLint, GLuint, GLenum, and GLboolean
#include <{{binding.identifier}}/{{binding.baseNamespace}}/functions-patches.h>
