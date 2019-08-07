
#pragma once


#include <functional>

#include <{{api.identifier}}binding/{{api.identifier}}binding_api.h>
#include <{{api.identifier}}binding/{{api.identifier}}binding_features.h>


namespace {{api.identifier}}binding
{


class {{api.identifier|upper}}BINDING_API Boolean32
{
public:
    using underlying_type = unsigned int;

public:
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean32();
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean32(bool on);
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean32(char on);
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean32(unsigned char on);
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean32(int on);
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Boolean32(unsigned int on);

    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator bool() const;
    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator char() const;
    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator unsigned char() const;
    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator int() const;
    {{api.identifier|upper}}BINDING_CONSTEXPR inline explicit operator unsigned int() const;

    inline Boolean32 & operator=(const Boolean32 & other);
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator<(const Boolean32 & other) const;
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator>(const Boolean32 & other) const;
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator<=(const Boolean32 & other) const;
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator>=(const Boolean32 & other) const;

    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator==(const Boolean32 & other) const;
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator!=(const Boolean32 & other) const;

public:
    underlying_type m_value;
};


} // namespace gl


#include <{{api.identifier}}binding/Boolean32.inl>
