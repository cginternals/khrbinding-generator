{{binding.baseNamespace}}{{binding.baseNamespace}}
namespace {{api}}
{


{{ucapi}}BINDING_CONSTEXPR inline bool operator==(const {{identifier}} & a, std::underlying_type<{{identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{identifier}}>::type>(a) == b;
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator!=(const {{identifier}} & a, std::underlying_type<{{identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{identifier}}>::type>(a) != b;
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator< (const {{identifier}} & a, std::underlying_type<{{identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{identifier}}>::type>(a) < b;
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator<=(const {{identifier}} & a, std::underlying_type<{{identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{identifier}}>::type>(a) <= b;
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator> (const {{identifier}} & a, std::underlying_type<{{identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{identifier}}>::type>(a) > b;
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator>=(const {{identifier}} & a, std::underlying_type<{{identifier}}>::type b)
{
    return static_cast<std::underlying_type<{{identifier}}>::type>(a) >= b;
}


{{ucapi}}BINDING_CONSTEXPR inline bool operator==(std::underlying_type<{{identifier}}>::type a, const {{identifier}} & b)
{
    return a == static_cast<std::underlying_type<{{identifier}}>::type>(b);
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator!=(std::underlying_type<{{identifier}}>::type a, const {{identifier}} & b)
{
    return a != static_cast<std::underlying_type<{{identifier}}>::type>(b);
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator< (std::underlying_type<{{identifier}}>::type a, const {{identifier}} & b)
{
    return a < static_cast<std::underlying_type<{{identifier}}>::type>(b);
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator<=(std::underlying_type<{{identifier}}>::type a, const {{identifier}} & b)
{
    return a <= static_cast<std::underlying_type<{{identifier}}>::type>(b);
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator> (std::underlying_type<{{identifier}}>::type a, const {{identifier}} & b)
{
    return a > static_cast<std::underlying_type<{{identifier}}>::type>(b);
}

{{ucapi}}BINDING_CONSTEXPR inline bool operator>=(std::underlying_type<{{identifier}}>::type a, const {{identifier}} & b)
{
    return a >= static_cast<std::underlying_type<{{identifier}}>::type>(b);
}


} // namespace {{api}}
