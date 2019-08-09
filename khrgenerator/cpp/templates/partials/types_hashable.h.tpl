
namespace std
{


template<>
struct hash<{{api.identifier}}::{{identifier}}>
{
    hash<std::underlying_type<{{api.identifier}}::{{identifier}}>::type>::result_type operator()(const {{api.identifier}}::{{identifier}} & t) const
    {
        return hash<std::underlying_type<{{api.identifier}}::{{identifier}}>::type>()(static_cast<std::underlying_type<{{api.identifier}}::{{identifier}}>::type>(t));
    }
};


} // namespace std