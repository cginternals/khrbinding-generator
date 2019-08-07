
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/extension.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


const std::unordered_map<{{profile.extensionType}}, std::set<std::string>> Meta_FunctionStringsByExtension =
{
{%- for extension in extensions|sort(attribute='identifier') %}{% if extension.requiredFunctions|length > 0 %}
    { {{profile.extensionType}}::{{extension.identifier}}, { {% for function in extension.requiredFunctions|sort(attribute='identifier') %}"{{function.identifier}}"{{ ", " if not loop.last }}{% endfor %} } }{{ "," if not loop.last }}
{%- endif %}{% endfor %}
};


} } // namespace {{api.identifier}}binding::aux
