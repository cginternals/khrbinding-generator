namespace {{binding.baseNamespace}}
{


std::ostream & operator<<(std::ostream & stream, const {{identifier}} & value)
{
    stream << {{profile.bindingNamespace}}::aux::bitfieldString<{{identifier}}>(value);
    return stream;
}


} // namespace {{binding.baseNamespace}}