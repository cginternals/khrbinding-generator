
#include <{{binding.bindingAuxIdentifier}}/types_to_string.h>

#include <ostream>
#include <bitset>
#include <sstream>

#include <{{binding.identifier}}/Version.h>
#include <{{binding.bindingAuxIdentifier}}/Meta.h>

#include "types_to_string_private.h"


namespace {{api.identifier}}
{

{% for group in enumerators|sort(attribute='identifier') %}
std::ostream & operator<<(std::ostream & stream, const {{group.identifier}} & value)
{
    stream << {{binding.bindingAuxNamespace}}::Meta::getString(value);
    return stream;
}
{% endfor -%}
{% for group in bitfields|sort(attribute='identifier') %}
std::ostream & operator<<(std::ostream & stream, const {{group.identifier}} & value)
{
    stream << {{binding.bindingAuxNamespace}}::bitfieldString<{{group.identifier}}>(value);
    return stream;
}
{% endfor %}

} // namespace {{api.identifier}}


namespace {{binding.namespace}}
{


template <>
std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::{{binding.enumType}}> & value)
{
    const auto & name = {{binding.auxNamespace}}::Meta::getString(value.value());
    stream.write(name.c_str(), static_cast<std::streamsize>(name.size()));

    return stream;
}

/*template <>
std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::{{binding.bitfieldType}}> & value)
{
    std::stringstream ss;
    ss << "0x" << std::hex << static_cast<unsigned>(value.value());
    stream << ss.str();

    return stream;
}*/

template <>
std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::{{binding.booleanType}}> & value)
{
    const auto & name = {{binding.auxNamespace}}::Meta::getString(value.value());
    stream.write(name.c_str(), static_cast<std::streamsize>(name.size()));

    return stream;
}

{% for cStringType in cStringTypes|sort %}
template <>
std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::{{cStringType}} *> & value)
{
    auto s = {{binding.auxNamespace}}::wrapString(reinterpret_cast<const char*>(value.value()));
    stream.write(s.c_str(), static_cast<std::streamsize>(s.size()));

    return stream;
}
{% endfor %}

std::ostream & operator<<(std::ostream & stream, const Version & version)
{
    stream << version.toString();

    return stream;
}

std::ostream & operator<<(std::ostream & stream, const AbstractValue * value)
{
    if (typeid(*value) == typeid(AbstractValue))
    {
        return stream << reinterpret_cast<const void*>(value);
    }
{% for cPointerType in cPointerTypes|sort %}
    if (typeid(*value) == typeid(Value<{{api.identifier}}::{{cPointerType}} *>))
    {
        return stream << *reinterpret_cast<const Value<{{api.identifier}}::{{cPointerType}} *>*>(value);
    }
{% endfor -%}
{% for type in types|sort(attribute='identifier') %}
    {{ "/*" if type.identifier.endswith("void") or type.identifier.startswith("_") }}
    if (typeid(*value) == typeid(Value<{{api.identifier}}::{{type.identifier}}>))
    {
        return stream << *reinterpret_cast<const Value<{{api.identifier}}::{{type.identifier}}>*>(value);
    }
    {{ "*/" if type.identifier.endswith("void") or type.identifier.startswith("_") }}
    
    if (typeid(*value) == typeid(Value<{{api.identifier}}::{{type.identifier}} *>))
    {
        return stream << *reinterpret_cast<const Value<{{api.identifier}}::{{type.identifier}} *>*>(value);
    }
{% endfor %}
    // expect an AbstractValue with a pointer in first member
    return stream << *reinterpret_cast<const Value<void *>*>(value);
}


} // namespace {{binding.namespace}}
