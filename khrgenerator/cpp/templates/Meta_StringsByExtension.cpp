
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/extension.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


const std::unordered_map<{{profile.extensionType}}, std::string> Meta_StringsByExtension =
{
{%- for extension in extensions|sort(attribute='identifier') %}
    { {{profile.extensionType}}::{{extension.identifier}}, "{{extension.identifier}}" }{{ "," if not loop.last }}
{%- endfor %}
};


} } // namespace {{api.identifier}}binding::aux
