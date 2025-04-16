
#include "Meta_Maps.h"

#include <{{binding.identifier}}/Version.h>


using namespace {{binding.baseNamespace}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


// all functions directly required by features, not indirectly via extensions

const std::map<Version, std::set<std::string>> Meta_FunctionStringsByVersion =
{
{%- for version in versions|sort %}
    { { {{version.majorVersion}}, {{version.minorVersion}} }, { {% for function in version.requiredFunctions|sort(attribute='identifier') %}"{{function.identifier}}"{{ ", " if not loop.last }}{% endfor %} } }{{ "," if not loop.last }}
{%- endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
