
#pragma once


#include <ostream>


namespace {{binding.namespace}}
{


template <typename T>
std::ostream & operator<<(std::ostream & stream, const Value<T> & value) {{profile.noexceptMacro}}
{
    stream << value.value();

    return stream;
}

template <typename T>
std::ostream & operator<<(std::ostream & stream, const Value<T *> & value) {{profile.noexceptMacro}}
{
    stream << std::hex << value.value() << std::dec;

    return stream;
}


} // namespace {{binding.namespace}}
