{{#integrations.valueRepresentable}}
{{^isStruct}}
    if (typeid(*value) == typeid(Value<{{binding.baseNamespace}}::{{identifier}}>))
    {
        return stream << *reinterpret_cast<const Value<{{binding.baseNamespace}}::{{identifier}}>*>(value);
    }
{{/isStruct}}
    if (typeid(*value) == typeid(Value<{{binding.baseNamespace}}::{{identifier}} *>))
    {
        return stream << *reinterpret_cast<const Value<{{binding.baseNamespace}}::{{identifier}} *>*>(value);
    }
{{/integrations.valueRepresentable}}{{^integrations.valueRepresentable}}
    // Omit {{binding.baseNamespace}}::{{identifier}}
{{/integrations.valueRepresentable}}
