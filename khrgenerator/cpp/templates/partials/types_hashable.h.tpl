
namespace std
{


template<>
struct hash<{{binding.baseNamespace}}::{{identifier}}>
{
    hash<std::underlying_type<{{binding.baseNamespace}}::{{identifier}}>::type>::result_type operator()(const {{binding.baseNamespace}}::{{identifier}} & t) const
    {
        return hash<std::underlying_type<{{binding.baseNamespace}}::{{identifier}}>::type>()(static_cast<std::underlying_type<{{binding.baseNamespace}}::{{identifier}}>::type>(t));
    }
};


} // namespace std