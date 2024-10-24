
#include <{{binding.bindingAuxIdentifier}}/types_to_string.h>

#include <ostream>
#include <bitset>
#include <sstream>

#include <{{binding.identifier}}/Version.h>
#include <{{binding.bindingAuxIdentifier}}/Meta.h>

#include "types_to_string_private.h"


namespace {{binding.baseNamespace}}
{

{% for group in enumerators|sort(attribute='identifier') %}
std::ostream & operator<<(std::ostream & stream, const {{group.identifier}} & value)
{
    const auto strings = {{binding.bindingAuxNamespace}}::Meta::getStrings(value);

    if (strings.size() == 0)
    {
        return stream;
    }

    stream << strings[0];

    for (auto i = static_cast<std::size_t>(1); i < strings.size(); ++i)
        stream << " | " << strings[i];

    return stream;
}
{% endfor -%}
{% for group in uniqueEnumerators|sort(attribute='identifier') %}
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

} // namespace {{binding.baseNamespace}}


namespace {{binding.namespace}}
{


template <>
std::ostream & operator<<(std::ostream & stream, const Value<{{binding.baseNamespace}}::{{binding.enumType}}> & value)
{
    stream << value.value();

    return stream;
}

/*template <>
std::ostream & operator<<(std::ostream & stream, const Value<{{binding.baseNamespace}}::{{binding.bitfieldType}}> & value)
{
    std::stringstream ss;
    ss << "0x" << std::hex << static_cast<unsigned>(value.value());
    stream << ss.str();

    return stream;
}*/

template <>
std::ostream & operator<<(std::ostream & stream, const Value<{{binding.baseNamespace}}::{{binding.booleanType}}> & value)
{
    const auto & name = {{binding.auxNamespace}}::Meta::getString(value.value());
    stream.write(name.c_str(), static_cast<std::streamsize>(name.size()));

    return stream;
}

template <>
std::ostream & operator<<(std::ostream & stream, const Value<const char *> & value)
{
    auto s = {{binding.auxNamespace}}::wrapString(value.value());
    stream.write(s.c_str(), static_cast<std::streamsize>(s.size()));

    return stream;
}

{% for cStringType in cStringTypes|sort %}
template <>
std::ostream & operator<<(std::ostream & stream, const Value<{{binding.baseNamespace}}::{{cStringType}} *> & value)
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
{% for nativeType in nativeTypes|sort %}
    if (typeid(*value) == typeid(Value<{{nativeType}}>))
    {
        return stream << *reinterpret_cast<const Value<{{nativeType}}>*>(value);
    }
{% endfor -%}
{% for cPointerType in cPointerTypes|sort %}
    if (typeid(*value) == typeid(Value<{{binding.baseNamespace}}::{{cPointerType}} *>))
    {
        return stream << *reinterpret_cast<const Value<{{binding.baseNamespace}}::{{cPointerType}} *>*>(value);
    }
{% endfor -%}
    if (typeid(*value) == typeid(Value<const char *>))
    {
        return stream << *reinterpret_cast<const Value<const char *>*>(value);
    }
{% for cStringType in cStringTypes|sort %}
    if (typeid(*value) == typeid(Value<{{binding.baseNamespace}}::{{cStringType}} *>))
    {
        return stream << *reinterpret_cast<const Value<{{binding.baseNamespace}}::{{cStringType}} *>*>(value);
    }
{% endfor -%}
{% for type in types|sort(attribute='identifier') %}
    {{ "/*" if type.identifier.endswith("void") or type.identifier.startswith("_") }}
    if (typeid(*value) == typeid(Value<{{binding.baseNamespace}}::{{type.identifier}}>))
    {
        return stream << *reinterpret_cast<const Value<{{binding.baseNamespace}}::{{type.identifier}}>*>(value);
    }
    {{ "*/" if type.identifier.endswith("void") or type.identifier.startswith("_") }}
    
    if (typeid(*value) == typeid(Value<{{binding.baseNamespace}}::{{type.identifier}} *>))
    {
        return stream << *reinterpret_cast<const Value<{{binding.baseNamespace}}::{{type.identifier}} *>*>(value);
    }
{% endfor %}
    // expect an AbstractValue with a pointer in first member
    return stream << *reinterpret_cast<const Value<void *>*>(value);
}


} // namespace {{binding.namespace}}
