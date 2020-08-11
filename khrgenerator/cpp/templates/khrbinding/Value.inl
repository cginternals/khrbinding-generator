
#pragma once


namespace
{


template <typename... Arguments>
struct ValueAdder;

template <>
struct ValueAdder<>
{
    inline static void add(std::vector<std::unique_ptr<{{binding.identifier}}::AbstractValue>> &) {{profile.noexceptMacro}}
    {
    }
};

template <typename Argument, typename... Arguments>
struct ValueAdder<Argument, Arguments...>
{
    inline static void add(std::vector<std::unique_ptr<{{binding.identifier}}::AbstractValue>> & values, Argument value, Arguments&&... rest) {{profile.noexceptMacro}}
    {
        values.push_back({{binding.identifier}}::createValue<Argument>(value));
        ValueAdder<Arguments...>::add(values, std::forward<Arguments>(rest)...);
    }
};

template <typename... Arguments>
inline void addValuesTo(std::vector<std::unique_ptr<{{binding.identifier}}::AbstractValue>> & values, Arguments&&... arguments) {{profile.noexceptMacro}}
{
    ValueAdder<Arguments...>::add(values, std::forward<Arguments>(arguments)...);
}


} // namespace


namespace {{binding.namespace}}
{


template <typename T>
{{binding.constexpr}} Value<T>::Value(const T & value) {{profile.noexceptMacro}}
: m_value(value)
{
}

template <typename T>
{{binding.constexpr}} T Value<T>::value() const {{profile.noexceptMacro}}
{
    return m_value;
}


template <typename Argument>
std::unique_ptr<AbstractValue> createValue(const Argument & argument) {{profile.noexceptMacro}}
{
    return std::unique_ptr<Value<Argument>>(new Value<Argument>(argument));
}

template <typename... Arguments>
std::vector<std::unique_ptr<AbstractValue>> createValues(Arguments&&... arguments) {{profile.noexceptMacro}}
{
    auto values = std::vector<std::unique_ptr<AbstractValue>>{};
    addValuesTo(values, std::forward<Arguments>(arguments)...);
    return values;
}


} // namespace {{binding.namespace}}
