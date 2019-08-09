namespace {{api.identifier}}
{


std::ostream & operator<<(std::ostream & stream, const {{identifier}} & value)
{
    stream << {{api.identifier}}binding::aux::bitfieldString<{{identifier}}>(value);
    return stream;
}


} // namespace {{api.identifier}}