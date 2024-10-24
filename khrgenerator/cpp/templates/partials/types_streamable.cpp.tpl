namespace {{binding.baseNamespace}}
{


std::ostream & operator<<(std::ostream & stream, const {{identifier}} & value)
{
    stream << {{binding.baseNamespace}}binding::aux::Meta::getString(value);
    return stream;
}


} // namespace {{binding.baseNamespace}}