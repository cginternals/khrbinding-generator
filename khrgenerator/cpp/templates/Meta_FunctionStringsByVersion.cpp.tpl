
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/Version.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


// all functions directly required by features, not indirectly via extensions

const std::map<Version, std::set<std::string>> Meta_FunctionStringsByVersion =
{
{%- for version in versions|sort %}
    { { {{version.majorVersion}}, {{version.minorVersion}} }, { {% for function in version.requiredFunctions|sort(attribute='identifier') %}"{{function.identifier}}"{{ ", " if not loop.last }}{% endfor %} } }{{ "," if not loop.last }}
{%- endfor %}
};


} } // namespace {{api.identifier}}binding::aux
