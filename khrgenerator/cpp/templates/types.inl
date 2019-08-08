
{% for group in basic_enumerators -%}
namespace std
{


template<>
struct hash<{{api.identifier}}::{{group.identifier}}>
{
    std::size_t operator()(const {{api.identifier}}::{{group.identifier}} & t) const
    {
        return hash<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>()(static_cast<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>(t));
    }
};


} // namespace std
{%- endfor %}


{% for group in generic_enumerators -%}
namespace std
{


template<>
struct hash<{{api.identifier}}::{{group.identifier}}>
{
    std::size_t operator()(const {{api.identifier}}::{{group.identifier}} & t) const
    {
        return hash<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>()(static_cast<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>(t));
    }
};


} // namespace std


namespace {{api.identifier}}
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


} // namespace {{api.identifier}}
{%- endfor %}


{% for group in bitfields -%}
namespace std
{


template<>
struct hash<{{api.identifier}}::{{group.identifier}}>
{
    std::size_t operator()(const {{api.identifier}}::{{group.identifier}} & t) const
    {
        return hash<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>()(static_cast<std::underlying_type<{{api.identifier}}::{{group.identifier}}>::type>(t));
    }
};


} // namespace std


namespace {{api.identifier}}
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


} // namespace {{api.identifier}}
{%- endfor %}
