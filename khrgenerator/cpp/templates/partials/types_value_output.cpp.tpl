{{#integrations.valueRepresentable}}
{{^isStruct}}
    if (typeid(*value) == typeid(Value<{{api.identifer}}::{{identifier}}>))
    {
        return stream << *reinterpret_cast<const Value<{{api.identifer}}::{{identifier}}>*>(value);
    }
{{/isStruct}}
    if (typeid(*value) == typeid(Value<{{api.identifer}}::{{identifier}} *>))
    {
        return stream << *reinterpret_cast<const Value<{{api.identifer}}::{{identifier}} *>*>(value);
    }
{{/integrations.valueRepresentable}}{{^integrations.valueRepresentable}}
    // Omit {{api.identifer}}::{{identifier}}
{{/integrations.valueRepresentable}}
