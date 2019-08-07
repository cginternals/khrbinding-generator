
#include <{{api.identifier}}binding-aux/ValidVersions.h>


const std::set<{{api.identifier}}binding::Version> {{api.identifier}}binding::aux::ValidVersions::s_validVersions =
{
{%- for version in versions %}
    { {{version.majorVersion}}, {{version.minorVersion}} }{% if not loop.last %},{% endif %}
{%- endfor %}
};

{% set latestVersion = versions[-1] -%}
const {{api.identifier}}binding::Version {{api.identifier}}binding::aux::ValidVersions::s_latest { {{latestVersion.majorVersion}}, {{latestVersion.minorVersion}} };
