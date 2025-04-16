
namespace {{binding.baseNamespace}}
{


{{ucapi}}BINDING_CONSTEXPR inline {{identifier}} operator+(const {{identifier}} & a, const std::underlying_type<{{identifier}}>::type b)
{
    return static_cast<{{identifier}}>(static_cast<std::underlying_type<{{identifier}}>::type>(a) + b);
}

{{ucapi}}BINDING_CONSTEXPR inline {{identifier}} operator-(const {{identifier}} & a, const std::underlying_type<{{identifier}}>::type b)
{
    return static_cast<{{identifier}}>(static_cast<std::underlying_type<{{identifier}}>::type>(a) - b);
}


} // namespace {{binding.baseNamespace}}
