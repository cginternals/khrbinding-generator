
#pragma once


#include <functional>

#include <{{api.identifier}}binding/{{api.identifier}}binding_api.h>
#include <{{api.identifier}}binding/{{api.identifier}}binding_features.h>


namespace {{api.identifier}}binding
{


/**
*  @brief
*    Boolean type based on an 8-bit integer
*/
class {{api.identifier|upper}}BINDING_API Boolean8
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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean8();

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean8(bool on);

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean8(char on);

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean8(unsigned char on);

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean8(int on);

    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] on
    *    Initial value
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean8(unsigned int on);

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `bool`
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator bool() const;

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `char`
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator char() const;

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `unsigned char`
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator unsigned char() const;

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `int`
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator int() const;

    /**
    *  @brief
    *    Type cast operator
    *
    *  @return
    *    %Value as `unsigned int`
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator unsigned int() const;

    /**
    *  @brief
    *    Copy assignment operator
    *
    *  @param[in] other
    *    %Value to copy from
    *
    *  @return
    *    This
    */
    inline Boolean8 & operator=(const Boolean8 & other);

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator<(const Boolean8 & other) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator>(const Boolean8 & other) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator<=(const Boolean8 & other) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator>=(const Boolean8 & other) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator==(const Boolean8 & other) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator!=(const Boolean8 & other) const;

public:
    underlying_type m_value; ///< %Value
};


} // namespace gl


#include <{{api.identifier}}binding/Boolean8.inl>
