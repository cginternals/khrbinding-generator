
#pragma once


#include <functional>

#include <{{binding}}/{{binding}}_api.h>
#include <{{binding}}/{{binding}}_features.h>


namespace {{binding}}
{


class {{ucbinding}}_API Boolean8
{
public:
    using underlying_type = unsigned char;

public:
    {{ucbinding}}_CONSTEXPR inline Boolean8();
    {{ucbinding}}_CONSTEXPR inline Boolean8(bool on);
    {{ucbinding}}_CONSTEXPR inline Boolean8(char on);
    {{ucbinding}}_CONSTEXPR inline Boolean8(unsigned char on);
    {{ucbinding}}_CONSTEXPR inline Boolean8(int on);
    {{ucbinding}}_CONSTEXPR inline Boolean8(unsigned int on);

    {{ucbinding}}_CONSTEXPR inline explicit operator bool() const;
    {{ucbinding}}_CONSTEXPR inline explicit operator char() const;
    {{ucbinding}}_CONSTEXPR inline explicit operator unsigned char() const;
    {{ucbinding}}_CONSTEXPR inline explicit operator int() const;
    {{ucbinding}}_CONSTEXPR inline explicit operator unsigned int() const;

    inline Boolean8 & operator=(const Boolean8 & other);
    {{ucbinding}}_CONSTEXPR inline bool operator<(const Boolean8 & other) const;
    {{ucbinding}}_CONSTEXPR inline bool operator>(const Boolean8 & other) const;
    {{ucbinding}}_CONSTEXPR inline bool operator<=(const Boolean8 & other) const;
    {{ucbinding}}_CONSTEXPR inline bool operator>=(const Boolean8 & other) const;

    {{ucbinding}}_CONSTEXPR inline bool operator==(const Boolean8 & other) const;
    {{ucbinding}}_CONSTEXPR inline bool operator!=(const Boolean8 & other) const;

public:
    underlying_type m_value;
};


} // namespace gl


#include <{{binding}}/Boolean8.inl>
