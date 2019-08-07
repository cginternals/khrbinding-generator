
#pragma once


namespace {{api.identifier}}binding
{


{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::Boolean8()
: Boolean8(false)
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::Boolean8(bool value)
: m_value(static_cast<underlying_type>(value))
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::Boolean8(char value)
: m_value(value)
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::Boolean8(unsigned char value)
: m_value(static_cast<underlying_type>(value))
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::Boolean8(int value)
: m_value(static_cast<underlying_type>(value))
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::Boolean8(unsigned int value)
: m_value(static_cast<underlying_type>(value))
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::operator bool() const
{
    return m_value != 0;
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::operator char() const
{
    return m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::operator unsigned char() const
{
    return m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::operator int() const
{
    return m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean8::operator unsigned int() const
{
    return m_value;
}

Boolean8 & Boolean8::operator=(const Boolean8 & other)
{
    m_value = other.m_value;

    return *this;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean8::operator<(const Boolean8 & other) const
{
    return m_value < other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean8::operator>(const Boolean8 & other) const
{
    return m_value > other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean8::operator<=(const Boolean8 & other) const
{
    return m_value <= other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean8::operator>=(const Boolean8 & other) const
{
    return m_value >= other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean8::operator==(const Boolean8 & other) const
{
    return m_value == other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean8::operator!=(const Boolean8 & other) const
{
    return m_value != other.m_value;
}


} // namespace {{api.identifier}}binding


namespace std
{


template<>
struct hash<{{api.identifier}}binding::Boolean8>
{
    std::size_t operator()(const {{api.identifier}}binding::Boolean8 & boolean) const
    {
        return hash<{{api.identifier}}binding::Boolean8::underlying_type>()(static_cast<{{api.identifier}}binding::Boolean8::underlying_type>(boolean));
    }
};


} // namespace std
