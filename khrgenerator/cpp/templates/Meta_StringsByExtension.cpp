
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{binding.baseNamespace}}/extension.h>


using namespace {{binding.baseNamespace}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


const std::unordered_map<{{binding.extensionType}}, std::string> Meta_StringsByExtension =
{
{%- for extension in extensions|sort(attribute='identifier') %}
    { {{binding.extensionType}}::{{extension.identifier}}, "{{extension.identifier}}" }{{ "," if not loop.last }}
{%- endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
