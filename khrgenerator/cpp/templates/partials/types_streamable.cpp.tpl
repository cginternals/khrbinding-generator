namespace {{api.identifier}}
{


std::ostream & operator<<(std::ostream & stream, const {{identifier}} & value)
{
    stream << {{api.identifier}}binding::aux::Meta::getString(value);
    return stream;
}


} // namespace {{api.identifier}}