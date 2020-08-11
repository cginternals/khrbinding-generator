
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
    {{binding.constexpr}} inline Boolean32() {{profile.noexceptMacro}};
    {{binding.constexpr}} inline Boolean32(bool on) {{profile.noexceptMacro}};
    {{binding.constexpr}} inline Boolean32(char on) {{profile.noexceptMacro}};
    {{binding.constexpr}} inline Boolean32(unsigned char on) {{profile.noexceptMacro}};
    {{binding.constexpr}} inline Boolean32(int on) {{profile.noexceptMacro}};
    {{binding.constexpr}} inline Boolean32(unsigned int on) {{profile.noexceptMacro}};

    {{binding.constexpr}} inline explicit operator bool() const {{profile.noexceptMacro}};
    {{binding.constexpr}} inline explicit operator char() const {{profile.noexceptMacro}};
    {{binding.constexpr}} inline explicit operator unsigned char() const {{profile.noexceptMacro}};
    {{binding.constexpr}} inline explicit operator int() const {{profile.noexceptMacro}};
    {{binding.constexpr}} inline explicit operator unsigned int() const {{profile.noexceptMacro}};

    {{binding.constexpr}} inline bool operator<(const Boolean32 & other) const {{profile.noexceptMacro}};
    {{binding.constexpr}} inline bool operator>(const Boolean32 & other) const {{profile.noexceptMacro}};
    {{binding.constexpr}} inline bool operator<=(const Boolean32 & other) const {{profile.noexceptMacro}};
    {{binding.constexpr}} inline bool operator>=(const Boolean32 & other) const {{profile.noexceptMacro}};

    {{binding.constexpr}} inline bool operator==(const Boolean32 & other) const {{profile.noexceptMacro}};
    {{binding.constexpr}} inline bool operator!=(const Boolean32 & other) const {{profile.noexceptMacro}};

public:
    underlying_type m_value;
};


} // namespace gl


#include <{{binding.identifier}}/Boolean32.inl>
