
#include "Meta_Maps.h"

#include <{{api.identifier}}binding/{{api.identifier}}/extension.h>
#include <{{api.identifier}}binding/Version.h>


using namespace {{api.identifier}};


namespace {{api.identifier}}binding { namespace aux
{


const std::unordered_map<{{profile.extensionType}}, Version> Meta_ReqVersionsByExtension =
{
{%- for extension, version in extensionsInCore|dictsort %}
    { {{profile.extensionType}}::{{extension.identifier}}, { {{version.majorVersion}}, {{version.minorVersion}} } }{{ "," if not loop.last }}
{%- endfor %}
};


} } // namespace {{api.identifier}}binding::aux
