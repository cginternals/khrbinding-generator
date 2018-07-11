
namespace std
{


template<>
struct hash<{{api}}::{{identifier}}>
{
    std::size_t operator()(const {{api}}::{{identifier}} & t) const
    {
        return hash<std::underlying_type<{{api}}::{{identifier}}>::type>()(static_cast<std::underlying_type<{{api}}::{{identifier}}>::type>(t));
    }
};


} // namespace std