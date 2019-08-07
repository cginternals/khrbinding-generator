
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{api.identifier}}/extension.h>


using namespace {{api.identifier}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


const std::unordered_map<{{binding.extensionType}}, std::set<std::string>> Meta_FunctionStringsByExtension =
{
{%- for extension in extensions|sort(attribute='identifier') %}{% if extension.requiredFunctions|length > 0 %}
    { {{binding.extensionType}}::{{extension.identifier}}, { {% for function in extension.requiredFunctions|sort(attribute='identifier') %}"{{function.identifier}}"{{ ", " if not loop.last }}{% endfor %} } }{{ "," if not loop.last }}
{%- endif %}{% endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
