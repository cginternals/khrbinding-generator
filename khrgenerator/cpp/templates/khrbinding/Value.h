
#pragma once


#include <vector>
#include <memory>

#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>

#include <{{binding.identifier}}/AbstractValue.h>


namespace {{binding.namespace}}
{


/**
*  @brief
*    The Value class represents a printable wrapper around an OpenGL data type
*
*  @tparam T
*    The data type of the wrapped value
*
*  @remark
*    This class is mainly used when callbacks of OpenGL functions are used
*/
template <typename T>
class {{binding.apiTemplateExport}} Value : public AbstractValue
{
public:
    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] value
    *    The value that should be printed later
    */
    {{binding.constexpr}} inline Value(const T & value) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    The deleted assigment operator
    *
    *  @remark
    *    For this dynamically allocated Value, no contents should be changable
    */
    Value & operator=(const Value &) = delete;

    /**
    *  @brief
    *    Get the value
    *
    *  @return
    *    The value
    */
    {{binding.constexpr}} inline T value() const {{profile.noexceptMacro}};

protected:
    const T m_value; ///< The value
};


/**
*  @brief
*    A wrapper around the type deduction and memory allocation of a specific argument
*
*  @tparam Argument
*    The type of the argument, usually an OpenGL data type.
*  @param[in] argument
*    The argument to wrap into a Value of type Argument.
*/
template <typename Argument>
inline std::unique_ptr<AbstractValue> createValue(const Argument & argument) {{profile.noexceptMacro}};

/**
*  @brief
*    A wrapper around the creation of a vector of arguments
*
*  @tparam Arguments
*    The types of the arguments, usually OpenGL data types
*  @param[in] arguments
*    The variadic parameter list of all arguments to convert
*
*  @remark
*    Internally uses the createValue() function
*/
template <typename... Arguments>
inline std::vector<std::unique_ptr<AbstractValue>> createValues(Arguments&&... arguments) {{profile.noexceptMacro}};


} // namespace {{binding.namespace}}


#include <{{binding.identifier}}/Value.inl>
