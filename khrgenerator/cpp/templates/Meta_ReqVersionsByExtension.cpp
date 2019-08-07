
#include "Meta_Maps.h"

#include <{{binding.identifier}}/{{api.identifier}}/extension.h>
#include <{{binding.identifier}}/Version.h>


using namespace {{api.identifier}};


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


const std::unordered_map<{{binding.extensionType}}, Version> Meta_ReqVersionsByExtension =
{
{%- for extension, version in extensionsInCore|dictsort %}
    { {{binding.extensionType}}::{{extension.identifier}}, { {{version.majorVersion}}, {{version.minorVersion}} } }{{ "," if not loop.last }}
{%- endfor %}
};


} } // namespace {{binding.bindingAuxNamespace}}
