
#include <gmock/gmock.h>

{% for version in versions|sort(attribute='identifier') %}
#include <{{binding.identifier}}/{{ version.identifier }}/{{binding.baseNamespace}}.h>
{%- endfor %}


TEST(AllVersions, Compilation)
{
    SUCCEED();  // compiling this file without errors and warnings results in successful test
}
