
#include <{{api.identifier}}binding-aux/Meta.h>

#include <{{api.identifier}}binding/{{api.identifier}}/bitfield.h>

#include "Meta_Maps.h"


using namespace {{api.identifier}};


namespace
{


const auto none = std::string{};


} // namespace


namespace {{api.identifier}}binding { namespace aux
{


{% for group in groups|sort(attribute='identifier') -%}

const std::string & Meta::getString(const {{group.identifier}} {{api.identifier}}bitfield)
{
    const auto i = Meta_StringsBy{{group.identifier}}.find({{api.identifier}}bitfield);
    if (i != Meta_StringsBy{{group.identifier}}.end())
    {
        return i->second;
    }
    return none;
}

{% endfor %}
} } // namespace {{api.identifier}}binding::aux
