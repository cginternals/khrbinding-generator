
#pragma once


#include <functional>

#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>


namespace {{binding.namespace}}
{


/**
*  @brief
*    Boolean type based on an 8-bit integer
*/
class {{binding.apiExport}} Boolean8
{
public:
    using underlying_type = unsigned char; ///< Type used for storing the value

public:
    /**
    *  @brief
    *    Constructor
    *
    *  @remark
    *    The value is set to `false`
    */
    {{binding.constexpr}} inline Boolean8() {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{binding.constexpr}} inline Boolean8(bool on) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{binding.constexpr}} inline Boolean8(char on) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{binding.constexpr}} inline Boolean8(unsigned char on) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{binding.constexpr}} inline Boolean8(int on) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{binding.constexpr}} inline Boolean8(unsigned int on) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `bool`
    */
    {{binding.constexpr}} inline explicit operator bool() const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `char`
    */
    {{binding.constexpr}} inline explicit operator char() const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `unsigned char`
    */
    {{binding.constexpr}} inline explicit operator unsigned char() const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `int`
    */
    {{binding.constexpr}} inline explicit operator int() const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `unsigned int`
    */
    {{binding.constexpr}} inline explicit operator unsigned int() const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Comparison operator
    *
    *  @param[in] other
    *    Other value
    *
    *  @return
    *    Result of comparing internal values
    *
    *  @remark
    *    Comparison uses numeric comparison of #underlying_type
    */
    {{binding.constexpr}} inline bool operator<(const Boolean8 & other) const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Comparison operator
    *
    *  @param[in] other
    *    Other value
    *
    *  @return
    *    Result of comparing internal values
    *
    *  @remark
    *    Comparison uses numeric comparison of #underlying_type
    */
    {{binding.constexpr}} inline bool operator>(const Boolean8 & other) const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Comparison operator
    *
    *  @param[in] other
    *    Other value
    *
    *  @return
    *    Result of comparing internal values
    *
    *  @remark
    *    Comparison uses numeric comparison of #underlying_type
    */
    {{binding.constexpr}} inline bool operator<=(const Boolean8 & other) const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Comparison operator
    *
    *  @param[in] other
    *    Other value
    *
    *  @return
    *    Result of comparing internal values
    *
    *  @remark
    *    Comparison uses numeric comparison of #underlying_type
    */
    {{binding.constexpr}} inline bool operator>=(const Boolean8 & other) const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Comparison operator
    *
    *  @param[in] other
    *    Other value
    *
    *  @return
    *    Result of comparing internal values
    *
    *  @remark
    *    Comparison uses numeric comparison of #underlying_type
    */
    {{binding.constexpr}} inline bool operator==(const Boolean8 & other) const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Comparison operator
    *
    *  @param[in] other
    *    Other value
    *
    *  @return
    *    Result of comparing internal values
    *
    *  @remark
    *    Comparison uses numeric comparison of #underlying_type
    */
    {{binding.constexpr}} inline bool operator!=(const Boolean8 & other) const {{profile.noexceptMacro}};

public:
    underlying_type m_value; ///< %Value
};


} // namespace gl


#include <{{binding.identifier}}/Boolean8.inl>
