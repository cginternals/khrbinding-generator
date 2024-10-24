
#include <{{binding.bindingAuxIdentifier}}/Meta.h>

#include <{{binding.identifier}}/{{binding.baseNamespace}}/bitfield.h>

#include "Meta_Maps.h"


using namespace {{binding.baseNamespace}};


namespace
{


const auto none = std::string{};


} // namespace


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


{% for group in groups|sort(attribute='identifier') -%}

const std::string & Meta::getString(const {{group.identifier}} {{binding.baseNamespace}}bitfield)
{
    const auto i = Meta_StringsBy{{group.identifier}}.find({{binding.baseNamespace}}bitfield);
    if (i != Meta_StringsBy{{group.identifier}}.end())
    {
        return i->second;
    }
    return none;
}

{% endfor %}
} } // namespace {{binding.bindingAuxNamespace}}
