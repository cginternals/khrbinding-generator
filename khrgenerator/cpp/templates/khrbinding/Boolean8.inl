
#pragma once


namespace {{binding.namespace}}
{


{{binding.constexpr}} Boolean8::Boolean8()
: Boolean8(false)
{
}

{{binding.constexpr}} Boolean8::Boolean8(bool value)
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean8::Boolean8(char value)
: m_value(value)
{
}

{{binding.constexpr}} Boolean8::Boolean8(unsigned char value)
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean8::Boolean8(int value)
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean8::Boolean8(unsigned int value)
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean8::operator bool() const
{
    return m_value != 0;
}

{{binding.constexpr}} Boolean8::operator char() const
{
    return m_value;
}

{{binding.constexpr}} Boolean8::operator unsigned char() const
{
    return m_value;
}

{{binding.constexpr}} Boolean8::operator int() const
{
    return m_value;
}

{{binding.constexpr}} Boolean8::operator unsigned int() const
{
    return m_value;
}

Boolean8 & Boolean8::operator=(const Boolean8 & other)
{
    m_value = other.m_value;

    return *this;
}

{{binding.constexpr}} bool Boolean8::operator<(const Boolean8 & other) const
{
    return m_value < other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator>(const Boolean8 & other) const
{
    return m_value > other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator<=(const Boolean8 & other) const
{
    return m_value <= other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator>=(const Boolean8 & other) const
{
    return m_value >= other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator==(const Boolean8 & other) const
{
    return m_value == other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator!=(const Boolean8 & other) const
{
    return m_value != other.m_value;
}


} // namespace {{binding.namespace}}


namespace std
{


template<>
struct hash<{{binding.identifier}}::Boolean8>
{
    std::size_t operator()(const {{binding.identifier}}::Boolean8 & boolean) const
    {
        return hash<{{binding.identifier}}::Boolean8::underlying_type>()(static_cast<{{binding.identifier}}::Boolean8::underlying_type>(boolean));
    }
};


} // namespace std
