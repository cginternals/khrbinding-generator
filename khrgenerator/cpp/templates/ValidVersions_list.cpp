
#include <{{binding.bindingAuxIdentifier}}/ValidVersions.h>


const std::set<{{binding.identifier}}::Version> {{binding.identifier}}::aux::ValidVersions::s_validVersions =
{
{%- for version in versions %}
    { {{version.majorVersion}}, {{version.minorVersion}} }{% if not loop.last %},{% endif %}
{%- endfor %}
};

{% set latestVersion = versions[-1] -%}
const {{binding.identifier}}::Version {{binding.identifier}}::aux::ValidVersions::s_latest { {{latestVersion.majorVersion}}, {{latestVersion.minorVersion}} };
