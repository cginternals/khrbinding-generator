
#pragma once


#include <{{binding.identifier}}/{{binding.baseNamespace}}/types.h>


{% for group in basic_enumerators|sort(attribute='identifier') -%}
namespace std
{


template<>
struct hash<{{binding.baseNamespace}}::{{group.identifier}}>
{
    std::size_t operator()(const {{binding.baseNamespace}}::{{group.identifier}} & t) const
    {
        return hash<std::underlying_type<{{binding.baseNamespace}}::{{group.identifier}}>::type>()(static_cast<std::underlying_type<{{binding.baseNamespace}}::{{group.identifier}}>::type>(t));
    }
};


} // namespace std
{%- endfor %}


{% for group in generic_enumerators|sort(attribute='identifier') -%}
namespace std
{


template<>
struct hash<{{binding.baseNamespace}}::{{group.identifier}}>
{
    std::size_t operator()(const {{binding.baseNamespace}}::{{group.identifier}} & t) const
    {
        return hash<std::underlying_type<{{binding.baseNamespace}}::{{group.identifier}}>::type>()(static_cast<std::underlying_type<{{binding.baseNamespace}}::{{group.identifier}}>::type>(t));
    }
};


} // namespace std


namespace {{binding.baseNamespace}}
{


{{binding.constexpr}} inline {{group.identifier}} operator+(const {{group.identifier}} & a, const std::underlying_type<{{group.identifier}}>::type b)
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) + b);
}

{{binding.constexpr}} inline {{group.identifier}} operator-(const {{group.identifier}} & a, const std::underlying_type<{{group.identifier}}>::type b)
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) - b);
}

{{binding.constexpr}} inline bool operator==(const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) == b;
}

{{binding.constexpr}} inline bool operator!=(const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) != b;
}

{{binding.constexpr}} inline bool operator< (const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) < b;
}

{{binding.constexpr}} inline bool operator<=(const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) <= b;
}

{{binding.constexpr}} inline bool operator> (const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) > b;
}

{{binding.constexpr}} inline bool operator>=(const {{group.identifier}} & a, std::underlying_type<{{group.identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{group.identifier}}>::type>(a) >= b;
}

{{binding.constexpr}} inline bool operator==(std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b)
{
    return a == static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator!=(std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b)
{
    return a != static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator< (std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b)
{
    return a < static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator<=(std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b)
{
    return a <= static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator> (std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b)
{
    return a > static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}

{{binding.constexpr}} inline bool operator>=(std::underlying_type<{{group.identifier}}>::type a, const {{group.identifier}} & b)
{
    return a >= static_cast<std::underlying_type<{{group.identifier}}>::type>(b);
}


} // namespace {{binding.baseNamespace}}
{%- endfor %}


{%- for group in bitfields|sort(attribute='identifier') %}


namespace std
{


template<>
struct hash<{{binding.baseNamespace}}::{{group.identifier}}>
{
    std::size_t operator()(const {{binding.baseNamespace}}::{{group.identifier}} & t) const
    {
        return hash<std::underlying_type<{{binding.baseNamespace}}::{{group.identifier}}>::type>()(static_cast<std::underlying_type<{{binding.baseNamespace}}::{{group.identifier}}>::type>(t));
    }
};


} // namespace std


namespace {{binding.baseNamespace}}
{


{{binding.constexpr}} inline {{group.identifier}} operator|(const {{group.identifier}} & a, const {{group.identifier}} & b)
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) | static_cast<std::underlying_type<{{group.identifier}}>::type>(b));
}

inline {{group.identifier}} & operator|=({{group.identifier}} & a, const {{group.identifier}} & b)
{
    a = static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) | static_cast<std::underlying_type<{{group.identifier}}>::type>(b));

    return a;
}

{{binding.constexpr}} inline {{group.identifier}} operator&(const {{group.identifier}} & a, const {{group.identifier}} & b)
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) & static_cast<std::underlying_type<{{group.identifier}}>::type>(b));
}

inline {{group.identifier}} & operator&=({{group.identifier}} & a, const {{group.identifier}} & b)
{
    a = static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) & static_cast<std::underlying_type<{{group.identifier}}>::type>(b));

    return a;
}

{{binding.constexpr}} inline {{group.identifier}} operator^(const {{group.identifier}} & a, const {{group.identifier}} & b)
{
    return static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) ^ static_cast<std::underlying_type<{{group.identifier}}>::type>(b));
}

inline {{group.identifier}} & operator^=({{group.identifier}} & a, const {{group.identifier}} & b)
{
    a = static_cast<{{group.identifier}}>(static_cast<std::underlying_type<{{group.identifier}}>::type>(a) ^ static_cast<std::underlying_type<{{group.identifier}}>::type>(b));

    return a;
}


} // namespace {{binding.baseNamespace}}
{%- endfor %}
