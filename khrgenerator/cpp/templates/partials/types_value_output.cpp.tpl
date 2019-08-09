{{#integrations.valueRepresentable}}
{{^isStruct}}
    if (typeid(*value) == typeid(Value<{{api.identifier}}::{{identifier}}>))
    {
        return stream << *reinterpret_cast<const Value<{{api.identifier}}::{{identifier}}>*>(value);
    }
{{/isStruct}}
    if (typeid(*value) == typeid(Value<{{api.identifier}}::{{identifier}} *>))
    {
        return stream << *reinterpret_cast<const Value<{{api.identifier}}::{{identifier}} *>*>(value);
    }
{{/integrations.valueRepresentable}}{{^integrations.valueRepresentable}}
    // Omit {{api.identifier}}::{{identifier}}
{{/integrations.valueRepresentable}}
