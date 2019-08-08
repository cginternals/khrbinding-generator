
namespace std
{


template<>
struct hash<{{api.identifer}}::{{identifier}}>
{
    hash<std::underlying_type<{{api.identifer}}::{{identifier}}>::type>::result_type operator()(const {{api.identifer}}::{{identifier}} & t) const
    {
        return hash<std::underlying_type<{{api.identifer}}::{{identifier}}>::type>()(static_cast<std::underlying_type<{{api.identifer}}::{{identifier}}>::type>(t));
    }
};


} // namespace std