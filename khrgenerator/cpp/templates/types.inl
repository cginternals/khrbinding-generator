
#pragma once


#include <{{binding.identifier}}/{{api.identifier}}/types.h>


{% for group in basic_enumerators|sort(attribute='identifier') -%}
namespace std
{


template<>
struct hash<{{api.identifier}}::{{group.identifier}}>
{
    std::size_t operator()(const {{api.identifier}}::{{group.identifier}} & t) const {{profile.noexceptMacro}}
    {
        return hash<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>()(static_cast<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>(t));
    }
};


} // namespace std
{%- endfor %}


{% for group in generic_enumerators|sort(attribute='identifier') -%}
namespace std
{


template<>
struct hash<{{api.identifier}}::{{group.identifier}}>
{
    std::size_t operator()(const {{api.identifier}}::{{group.identifier}} & t) const {{profile.noexceptMacro}}
    {
        return hash<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>()(static_cast<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>(t));
    }
};


} // namespace std


namespace {{api.identifier}}
{


{{binding.constexpr}} inline {{group.identifier}} operator+(const {{group.identifier}} & a, const std::underlying_type<{{group.identifier}}>::type b) {{profile.noexceptMacro}}
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) + b);
}

{{binding.constexpr}} inline {{group.identifier}} operator-(const {{group.identifier}} & a, const std::underlying_type<{{group.identifier}}>::type b) {{profile.noexceptMacro}}
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) - b);
}

{{binding.constexpr}} inline bool operator==(const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b) {{profile.noexceptMacro}}
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) == b;
}

{{binding.constexpr}} inline bool operator!=(const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b) {{profile.noexceptMacro}}
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) != b;
}

{{binding.constexpr}} inline bool operator< (const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b) {{profile.noexceptMacro}}
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) < b;
}

{{binding.constexpr}} inline bool operator<=(const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b) {{profile.noexceptMacro}}
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) <= b;
}

{{binding.constexpr}} inline bool operator> (const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b) {{profile.noexceptMacro}}
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) > b;
}

{{binding.constexpr}} inline bool operator>=(const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b) {{profile.noexceptMacro}}
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) >= b;
}

{{binding.constexpr}} inline bool operator==(std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    return a == static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator!=(std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    return a != static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator< (std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    return a < static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator<=(std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    return a <= static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator> (std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    return a > static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator>=(std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    return a >= static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}


} // namespace {{api.identifier}}
{%- endfor %}


{%- for group in bitfields|sort(attribute='identifier') %}


namespace std
{


template<>
struct hash<{{api.identifier}}::{{group.identifier}}>
{
    std::size_t operator()(const {{api.identifier}}::{{group.identifier}} & t) const {{profile.noexceptMacro}}
    {
        return hash<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>()(static_cast<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>(t));
    }
};


} // namespace std


namespace {{api.identifier}}
{


{{binding.constexpr}} inline {{group.identifier}} operator|(const {{group.identifier}} & a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) | static_cast<std::underlying_type<{{group.identifier}}>::type>(b));
}

inline {{group.identifier}} & operator|=({{group.identifier}} & a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    a = static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) | static_cast<std::underlying_type<{{group.identifier}}>::type>(b));

    return a;
}

{{binding.constexpr}} inline {{group.identifier}} operator&(const {{group.identifier}} & a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) & static_cast<std::underlying_type<{{group.identifier}}>::type>(b));
}

inline {{group.identifier}} & operator&=({{group.identifier}} & a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    a = static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) & static_cast<std::underlying_type<{{group.identifier}}>::type>(b));

    return a;
}

{{binding.constexpr}} inline {{group.identifier}} operator^(const {{group.identifier}} & a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) ^ static_cast<std::underlying_type<{{group.identifier}}>::type>(b));
}

inline {{group.identifier}} & operator^=({{group.identifier}} & a, const {{group.identifier}} & b) {{profile.noexceptMacro}}
{
    a = static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) ^ static_cast<std::underlying_type<{{group.identifier}}>::type>(b));

    return a;
}


} // namespace {{api.identifier}}
{%- endfor %}
