{{#integrations.valueRepresentable}}
{{^isStruct}}
    if (typeid(*value) == typeid(Value<{{api}}::{{identifier}}>))
    {
        return stream << *reinterpret_cast<const Value<{{api}}::{{identifier}}>*>(value);
    }
{{/isStruct}}
    if (typeid(*value) == typeid(Value<{{api}}::{{identifier}} *>))
    {
        return stream << *reinterpret_cast<const Value<{{api}}::{{identifier}} *>*>(value);
    }
{{/integrations.valueRepresentable}}{{^integrations.valueRepresentable}}
    // Omit {{api}}::{{identifier}}
{{/integrations.valueRepresentable}}
