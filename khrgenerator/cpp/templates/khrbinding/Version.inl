
#pragma once


namespace {{binding.namespace}}
{


{{binding.constexpr}} Version::Version() {{profile.noexceptMacro}}
: m_major(0)
, m_minor(0)
{
}

{{binding.constexpr}} Version::Version(unsigned char majorVersion, unsigned char minorVersion) {{profile.noexceptMacro}}
: m_major(majorVersion)
, m_minor(minorVersion)
{
}

{{binding.constexpr}} Version::Version(const Version & version) {{profile.noexceptMacro}}
: Version(version.m_major, version.m_minor)
{
}

Version::Version(Version && version) {{profile.noexceptMacro}}
: Version(std::move(version.m_major), std::move(version.m_minor))
{
}


{{binding.constexpr}} unsigned char Version::majorVersion() const {{profile.noexceptMacro}}
{
    return m_major;
}

{{binding.constexpr}} unsigned char Version::minorVersion() const {{profile.noexceptMacro}}
{
    return m_minor;
}

Version::operator std::pair<unsigned char, unsigned char>() const {{profile.noexceptMacro}}
{
    return std::pair<unsigned char, unsigned char>(m_major, m_minor);
}

Version::operator std::pair<unsigned short, unsigned short>() const {{profile.noexceptMacro}}
{
    return std::pair<unsigned short, unsigned short>(m_major, m_minor);
}

Version::operator std::pair<unsigned int, unsigned int>() const {{profile.noexceptMacro}}
{
    return std::pair<unsigned int, unsigned int>(m_major, m_minor);
}

std::string Version::toString() const {{profile.noexceptMacro}}
{
    if (isNull()) {
        return "-.-";
    }

    return std::to_string(static_cast<int>(m_major)) + '.'  + std::to_string(static_cast<int>(m_minor));
}

{{binding.constexpr}} bool Version::isNull() const {{profile.noexceptMacro}}
{
    return m_major == 0;
}

Version & Version::operator=(const Version & version) {{profile.noexceptMacro}}
{
    m_major = version.m_major;
    m_minor = version.m_minor;

    return *this;
}

Version & Version::operator=(Version && version) {{profile.noexceptMacro}}
{
    m_major = std::move(version.m_major);
    m_minor = std::move(version.m_minor);

    return *this;
}

{{binding.constexpr}} bool Version::operator<(const Version & version) const {{profile.noexceptMacro}}
{
    return m_major < version.m_major
        || (m_major == version.m_major && m_minor < version.m_minor);
}

{{binding.constexpr}} bool Version::operator>(const Version & version) const {{profile.noexceptMacro}}
{
    return m_major > version.m_major
        || (m_major == version.m_major && m_minor > version.m_minor);
}

{{binding.constexpr}} bool Version::operator==(const Version & version) const {{profile.noexceptMacro}}
{
    return m_major == version.m_major
        && m_minor == version.m_minor;
}

{{binding.constexpr}} bool Version::operator!=(const Version & version) const {{profile.noexceptMacro}}
{
    return m_major != version.m_major
        || m_minor != version.m_minor;
}

{{binding.constexpr}} bool Version::operator>=(const Version & version) const {{profile.noexceptMacro}}
{
    return *this > version || *this == version;
}

{{binding.constexpr}} bool Version::operator<=(const Version & version) const {{profile.noexceptMacro}}
{
    return *this < version || *this == version;
}


} // namespace {{binding.namespace}}
