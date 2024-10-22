
#pragma once


#include <string>
#include <set>
#include <utility>

#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>


namespace {{binding.namespace}}
{


/**
*  @brief
*    The Version class represents an OpenGL feature, consisting of major version and minor version, excluding the profile information.
*
*    This instance can represent both any officially released OpenGL feature and other combinations of major and minor version, and provides methods for validity checking and comparison
*
*  Example code:
*  @code{.cpp}
*  const {{binding.namespace}}::Version currentVersion = {{binding.namespace}}::aux::ContextInfo::version();
*
*  if (currentVersion >= {{binding.namespace}}::Version(3, 2))
*  {
*      // do something
*  }
*  @endcode
*/
class {{binding.apiTemplateExport}} Version
{
public:
    /**
    *  @brief
    *    Default constructor, resulting in an invalid Version object
    */
    {{binding.constexpr}} inline Version();

    /**
    *  @brief
    *    Constructor for a Version object with the given major and minor version
    *
    *  @param[in] majorVersion
    *    The major version
    *  @param[in] minorVersion
    *    The minor version
    */
    {{binding.constexpr}} inline Version(unsigned char majorVersion, unsigned char minorVersion);

    /**
    *  @brief
    *    Copy constructor
    *
    *  @param[in] version
    *    The Version the data is used from
    */
    {{binding.constexpr}} inline Version(const Version & version);

    /**
    *  @brief
    *    Move constructor
    *
    *  @param[in] version
    *    The Version the data is moved from
    */
    inline Version(Version && version);

    /**
    *  @brief
    *    Accessor for the major version
    *
    *  @return
    *    The major version
    */
    {{binding.constexpr}} inline unsigned char majorVersion() const;

    /**
    *  @brief
    *    Accessor for the minor version
    *
    *  @return
    *    The minor version
    */
    {{binding.constexpr}} inline unsigned char minorVersion() const;

    /**
    *  @brief
    *    Cast operator for a std::pair cast of type unsigned char
    */
    inline operator std::pair<unsigned char, unsigned char>() const;

    /**
    *  @brief
    *    Cast operator for a std::pair cast of type unsigned short
    */
    inline operator std::pair<unsigned short, unsigned short>() const;

    /**
    *  @brief
    *    Cast operator for a std::pair cast of type unsigned int
    */
    inline operator std::pair<unsigned int, unsigned int>() const;

    /**
    *  @brief
    *    Create a string representing the Version using the scheme "<majorVersion>.<minorVersion>"
    *
    *  @return
    *    The version as string, "-.-" iff the Version is invalid
    */
    inline std::string toString() const;

    /**
    *  @brief
    *    Check if the Version was constructed using the default constructor
    *
    *  @return
    *    `true` if the major version is 0, else `false`
    *
    *  @remark
    *    This method can be used to check if this Version was constructed using the default constructor or is otherwise malformed
    */
    {{binding.constexpr}} inline bool isNull() const;

    /**
    *  @brief
    *    The assignment operator of another Version
    *
    *  @param[in] version
    *    The version the data is used from
    *
    *  @return
    *    The reference to this Version
    */
    inline Version & operator=(const Version & version);

    /**
    *  @brief
    *    The assignment operator of another Version that is moved from
    *
    *  @param[in] version
    *    The version the data is moved from
    *
    *  @return
    *    The reference to this Version
    */
    inline Version & operator=(Version && version);

    /**
    *  @brief
    *    Operator for lesser comparison to another Version
    *
    *  @param[in] version
    *    The Version to compare to
    *
    *  @return
    *    `true` if this Version is lower than the other Version, else `false`
    */
    {{binding.constexpr}} inline bool operator<(const Version & version) const;

    /**
    *  @brief
    *    Operator for greater comparison to another Version
    *
    *  @param[in] version
    *    The Version to compare to
    *
    *  @return
    *    `true` if this Version is greater than the other Version, else `false`
    */
    {{binding.constexpr}} inline bool operator>(const Version & version) const;

    /**
    *  @brief
    *    Operator for equal comparison to another Version
    *
    *  @param[in] version
    *    The Version to compare to
    *
    *  @return
    *    `true` if this Version is equal to the other Version, else `false`
    */
    {{binding.constexpr}} inline bool operator==(const Version & version) const;

    /**
    *  @brief
    *    Operator for unequal comparison to another Version
    *
    *  @param[in] version
    *    The Version to compare to
    *
    *  @return
    *    `true` if this Version is not equal to the other Version, else `false`
    */
    {{binding.constexpr}} inline bool operator!=(const Version & version) const;

    /**
    *  @brief
    *    Operator for greater equal comparison to another Version
    *
    *  @param[in] version
    *    The Version to compare to
    *
    *  @return
    *    `true` if this Version is greater than or equal to the other Version, else `false`
    */
    {{binding.constexpr}} inline bool operator>=(const Version & version) const;

    /**
    *  @brief
    *    Operator for lesser equal comparison to another Version
    *
    *  @param[in] version
    *    The Version to compare to
    *
    *  @return
    *    `true` if this Version is lower than or equal to the other Version, else `false`
    */
    {{binding.constexpr}} inline bool operator<=(const Version & version) const;


protected:
    unsigned char m_major; ///< The major version
    unsigned char m_minor; ///< The minor version
};


} // namespace {{binding.namespace}}


#include <{{binding.identifier}}/Version.inl>
