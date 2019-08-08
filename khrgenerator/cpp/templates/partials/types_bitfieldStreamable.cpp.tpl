namespace {{api.identifer}}
{


std::ostream & operator<<(std::ostream & stream, const {{identifier}} & value)
{
    stream << {{api.identifer}}binding::aux::bitfieldString<{{identifier}}>(value);
    return stream;
}


} // namespace {{api.identifer}}