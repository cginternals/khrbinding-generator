
#pragma once


#include <functional>

#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>


namespace {{binding.namespace}}
{


class {{binding.apiExport}} Boolean32
{
public:
    using underlying_type = unsigned int;

public:
    {{binding.constexpr}} inline Boolean32();
    {{binding.constexpr}} inline Boolean32(const Boolean32 & other);
    {{binding.constexpr}} inline Boolean32(bool on);
    {{binding.constexpr}} inline Boolean32(char on);
    {{binding.constexpr}} inline Boolean32(unsigned char on);
    {{binding.constexpr}} inline Boolean32(int on);
    {{binding.constexpr}} inline Boolean32(unsigned int on);

    {{binding.constexpr}} inline explicit operator bool() const;
    {{binding.constexpr}} inline explicit operator char() const;
    {{binding.constexpr}} inline explicit operator unsigned char() const;
    {{binding.constexpr}} inline explicit operator int() const;
    {{binding.constexpr}} inline explicit operator unsigned int() const;

    inline Boolean32 & operator=(const Boolean32 & other);
    {{binding.constexpr}} inline bool operator<(const Boolean32 & other) const;
    {{binding.constexpr}} inline bool operator>(const Boolean32 & other) const;
    {{binding.constexpr}} inline bool operator<=(const Boolean32 & other) const;
    {{binding.constexpr}} inline bool operator>=(const Boolean32 & other) const;

    {{binding.constexpr}} inline bool operator==(const Boolean32 & other) const;
    {{binding.constexpr}} inline bool operator!=(const Boolean32 & other) const;

public:
    underlying_type m_value;
};


} // namespace gl


#include <{{binding.identifier}}/Boolean32.inl>
