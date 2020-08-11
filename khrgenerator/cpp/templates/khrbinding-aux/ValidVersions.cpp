
#include <{{binding.bindingAuxIdentifier}}/ValidVersions.h>


namespace {{binding.namespace}} { namespace {{binding.auxNamespace}}
{


bool ValidVersions::isValid(const Version & version) {{profile.noexceptMacro}}
{
    return s_validVersions.find(version) != s_validVersions.end();
}

const Version & ValidVersions::nearest(const Version & version) {{profile.noexceptMacro}}
{
    auto iterator = s_validVersions.lower_bound(version);

    if (iterator == s_validVersions.end())
    {
        return *(--iterator);
    }

    return *iterator;
}

const Version & ValidVersions::latest() {{profile.noexceptMacro}}
{
    return s_latest;
}

const std::set<Version> & ValidVersions::versions() {{profile.noexceptMacro}}
{
    return s_validVersions;
}

std::set<Version> ValidVersions::preceeding(const Version & version) {{profile.noexceptMacro}}
{
    auto preceedingVersions = std::set<Version>{};
    for (auto & v : s_validVersions)
    {
        if (v < version)
        {
            preceedingVersions.insert(v);
        }
    }

    return preceedingVersions;
}

std::set<Version> ValidVersions::succeeding(const Version & version) {{profile.noexceptMacro}}
{
    auto succeedingVersions = std::set<Version>{};
    for (auto & v : s_validVersions)
    {
        if (v > version)
        {
            succeedingVersions.insert(v);
        }
    }

    return succeedingVersions;
}


} } // namespace {{binding.bindingAuxNamespace}}
