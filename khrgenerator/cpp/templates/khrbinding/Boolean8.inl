
#pragma once


namespace {{binding.namespace}}
{


{{binding.constexpr}} Boolean8::Boolean8() {{profile.noexceptMacro}}
: Boolean8(false)
{
}

{{binding.constexpr}} Boolean8::Boolean8(bool value) {{profile.noexceptMacro}}
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean8::Boolean8(char value) {{profile.noexceptMacro}}
: m_value(value)
{
}

{{binding.constexpr}} Boolean8::Boolean8(unsigned char value) {{profile.noexceptMacro}}
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean8::Boolean8(int value) {{profile.noexceptMacro}}
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean8::Boolean8(unsigned int value) {{profile.noexceptMacro}}
: m_value(static_cast<underlying_type>(value))
{
}

{{binding.constexpr}} Boolean8::operator bool() const {{profile.noexceptMacro}}
{
    return m_value != 0;
}

{{binding.constexpr}} Boolean8::operator char() const {{profile.noexceptMacro}}
{
    return m_value;
}

{{binding.constexpr}} Boolean8::operator unsigned char() const {{profile.noexceptMacro}}
{
    return m_value;
}

{{binding.constexpr}} Boolean8::operator int() const {{profile.noexceptMacro}}
{
    return m_value;
}

{{binding.constexpr}} Boolean8::operator unsigned int() const {{profile.noexceptMacro}}
{
    return m_value;
}

{{binding.constexpr}} bool Boolean8::operator<(const Boolean8 & other) const {{profile.noexceptMacro}}
{
    return m_value < other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator>(const Boolean8 & other) const {{profile.noexceptMacro}}
{
    return m_value > other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator<=(const Boolean8 & other) const {{profile.noexceptMacro}}
{
    return m_value <= other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator>=(const Boolean8 & other) const {{profile.noexceptMacro}}
{
    return m_value >= other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator==(const Boolean8 & other) const {{profile.noexceptMacro}}
{
    return m_value == other.m_value;
}

{{binding.constexpr}} bool Boolean8::operator!=(const Boolean8 & other) const {{profile.noexceptMacro}}
{
    return m_value != other.m_value;
}


} // namespace {{binding.namespace}}


namespace std
{


template<>
struct hash<{{binding.identifier}}::Boolean8>
{
    std::size_t operator()(const {{binding.identifier}}::Boolean8 & boolean) const {{profile.noexceptMacro}}
    {
        return hash<{{binding.identifier}}::Boolean8::underlying_type>()(static_cast<{{binding.identifier}}::Boolean8::underlying_type>(boolean));
    }
};


} // namespace std
