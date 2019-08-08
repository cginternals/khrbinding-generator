namespace {{api.identifer}}
{


std::ostream & operator<<(std::ostream & stream, const {{identifier}} & value)
{
    stream << {{api.identifer}}binding::aux::Meta::getString(value);
    return stream;
}


} // namespace {{api.identifer}}