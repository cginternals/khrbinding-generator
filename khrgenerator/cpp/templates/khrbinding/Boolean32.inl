
#pragma once


namespace {{binding.namespace}}
{


{{binding.constexpr}} Boolean32::Boolean32()
: Boolean32(false)
{
}

{{binding.constexpr}} Boolean32::Boolean32(const Boolean32 & other)
: m_value(other.m_value)
{
}

{{binding.constexpr}} Boolean32::Boolean32(bool value)
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean32::Boolean32(char value)
: m_value(value)
{
}

{{binding.constexpr}} Boolean32::Boolean32(unsigned char value)
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean32::Boolean32(int value)
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean32::Boolean32(unsigned int value)
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean32::operator bool() const
{
    return m_value != 0;
}

{{binding.constexpr}} Boolean32::operator char() const
{
    return m_value;
}

{{binding.constexpr}} Boolean32::operator unsigned char() const
{
    return m_value;
}

{{binding.constexpr}} Boolean32::operator int() const
{
    return m_value;
}

{{binding.constexpr}} Boolean32::operator unsigned int() const
{
    return m_value;
}

Boolean32 & Boolean32::operator=(const Boolean32 & other)
{
    m_value = other.m_value;

    return *this;
}

{{binding.constexpr}} bool Boolean32::operator<(const Boolean32 & other) const
{
    return m_value < other.m_value;
}

{{binding.constexpr}} bool Boolean32::operator>(const Boolean32 & other) const
{
    return m_value > other.m_value;
}

{{binding.constexpr}} bool Boolean32::operator<=(const Boolean32 & other) const
{
    return m_value <= other.m_value;
}

{{binding.constexpr}} bool Boolean32::operator>=(const Boolean32 & other) const
{
    return m_value >= other.m_value;
}

{{binding.constexpr}} bool Boolean32::operator==(const Boolean32 & other) const
{
    return m_value == other.m_value;
}

{{binding.constexpr}} bool Boolean32::operator!=(const Boolean32 & other) const
{
    return m_value != other.m_value;
}


} // namespace {{binding.namespace}}


namespace std
{


template<>
struct hash<{{binding.identifier}}::Boolean32>
{
    std::size_t operator()(const {{binding.identifier}}::Boolean32 & boolean) const
    {
        return hash<{{binding.identifier}}::Boolean32::underlying_type>()(static_cast<{{binding.identifier}}::Boolean32::underlying_type>(boolean));
    }
};


} // namespace std
