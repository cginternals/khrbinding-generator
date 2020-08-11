
#include <{{binding.bindingAuxIdentifier}}/Meta.h>

#include <{{binding.identifier}}/{{api.identifier}}/bitfield.h>

#include "Meta_Maps.h"


using namespace {{api.identifier}};


namespace
{


const auto none = std::string{};


} // namespace


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


{% for group in groups|sort(attribute='identifier') -%}

const std::string & Meta::getString(const {{group.identifier}} {{api.identifier}}bitfield) {{profile.noexceptMacro}}
{
    const auto i = Meta_StringsBy{{group.identifier}}.find({{api.identifier}}bitfield);
    if (i != Meta_StringsBy{{group.identifier}}.end())
    {
        return i->second;
    }
    return none;
}

{% endfor %}
} } // namespace {{binding.bindingAuxNamespace}}
