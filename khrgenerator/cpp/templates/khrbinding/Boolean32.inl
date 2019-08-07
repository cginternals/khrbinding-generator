
#pragma once


namespace {{api.identifier}}binding
{


{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::Boolean32()
: Boolean32(false)
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::Boolean32(bool value)
: m_value(static_cast<underlying_type>(value))
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::Boolean32(char value)
: m_value(value)
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::Boolean32(unsigned char value)
: m_value(static_cast<underlying_type>(value))
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::Boolean32(int value)
: m_value(static_cast<underlying_type>(value))
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::Boolean32(unsigned int value)
: m_value(static_cast<underlying_type>(value))
{
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::operator bool() const
{
    return m_value != 0;
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::operator char() const
{
    return m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::operator unsigned char() const
{
    return m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::operator int() const
{
    return m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR Boolean32::operator unsigned int() const
{
    return m_value;
}

Boolean32 & Boolean32::operator=(const Boolean32 & other)
{
    m_value = other.m_value;

    return *this;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean32::operator<(const Boolean32 & other) const
{
    return m_value < other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean32::operator>(const Boolean32 & other) const
{
    return m_value > other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean32::operator<=(const Boolean32 & other) const
{
    return m_value <= other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean32::operator>=(const Boolean32 & other) const
{
    return m_value >= other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean32::operator==(const Boolean32 & other) const
{
    return m_value == other.m_value;
}

{{api.identifier|upper}}BINDING_CONSTEXPR bool Boolean32::operator!=(const Boolean32 & other) const
{
    return m_value != other.m_value;
}


} // namespace {{api.identifier}}binding


namespace std
{


template<>
struct hash<{{api.identifier}}binding::Boolean32>
{
    std::size_t operator()(const {{api.identifier}}binding::Boolean32 & boolean) const
    {
        return hash<{{api.identifier}}binding::Boolean32::underlying_type>()(static_cast<{{api.identifier}}binding::Boolean32::underlying_type>(boolean));
    }
};


} // namespace std
