
{% if binding.headerGuardMacro|length > 0 %}
#if {% for macro in binding.headerGuardMacro %}defined({{ macro }}){{ " || " if not loop.last }}{% endfor %}
    #error "{{binding.identifier}} is not compatible with {% for replacement in binding.headerReplacement %}{{ replacement }}{{ ", " if not loop.last }}{% endfor %}"
#endif
{% endif %}
