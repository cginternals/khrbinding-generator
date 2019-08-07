
#pragma once


#include <string>
#include <set>
#include <utility>

#include <{{api.identifier}}binding/{{api.identifier}}binding_api.h>
#include <{{api.identifier}}binding/{{api.identifier}}binding_features.h>


namespace {{api.identifier}}binding
{


/**
*  @brief
*    The Version class represents an OpenGL feature, consisting of major version and minor version, excluding the profile information.
*
*    This instance can represent both any officially released OpenGL feature and other combinations of major and minor version, and provides methods for validity checking and comparison
*
*  Example code:
*  @code{.cpp}
*  const glbinding::Version currentVersion = glbinding::aux::ContextInfo::version();
*
*  if (currentVersion >= glbinding::Version(3, 2))
*  {
*      // do something
*  }
*  @endcode
*/
class {{api.identifier|upper}}BINDING_TEMPLATE_API Version
{
public:
    /**
    *  @brief
    *    Default constructor, resulting in an invalid Version object
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Version();

    /**
    *  @brief
    *    Constructor for a Version object with the given major and minor version
    *
    *  @param[in] majorVersion
    *    The major version
    *  @param[in] minorVersion
    *    The minor version
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Version(unsigned char majorVersion, unsigned char minorVersion);

    /**
    *  @brief
    *    Copy constructor
    *
    *  @param[in] version
    *    The Version the data is used from
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline Version(const Version & version);

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline unsigned char majorVersion() const;

    /**
    *  @brief
    *    Accessor for the minor version
    *
    *  @return
    *    The minor version
    */
    {{api.identifier|upper}}BINDING_CONSTEXPR inline unsigned char minorVersion() const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool isNull() const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator<(const Version & version) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator>(const Version & version) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator==(const Version & version) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator!=(const Version & version) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator>=(const Version & version) const;

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
    {{api.identifier|upper}}BINDING_CONSTEXPR inline bool operator<=(const Version & version) const;


protected:
    unsigned char m_major; ///< The major version
    unsigned char m_minor; ///< The minor version
};


} // namespace {{api.identifier}}binding


#include <{{api.identifier}}binding/Version.inl>
