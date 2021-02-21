
#pragma once


#include <string>
#include <utility>
#include <vector>
#include <set>
#include <cstdint>

#include <{{binding.bindingAuxIdentifier}}/{{binding.bindingAuxIdentifier}}_api.h>
#include <{{binding.bindingAuxIdentifier}}/{{binding.bindingAuxIdentifier}}_features.h>

#include <{{binding.identifier}}/{{api.identifier}}/types.h>
#include <{{binding.identifier}}/AbstractFunction.h>


namespace {{binding.namespace}}
{


class Version;


namespace {{binding.auxNamespace}}
{


/**
*  @brief
*    Provisioning of meta information about OpenGL extensions, functions and conversion of strings and symbols of the OpenGL API
*/
class {{binding.auxApiExport}} Meta
{
public:
    /**
    *  @brief
    *    Deleted Constructor as all functions are static
    */
    Meta() = delete;

    /**
    *  @brief
    *    Returns the revision of the parsed {{profile.inputfile}} file
    *
    *  @return
    *    The revision of the parsed {{profile.inputfile}} file
    */
    static int {{api.identifier}}Revision();

    /**
    *  @brief
    *    Converts a string into a bitfield symbol
    *
    *  @param[in] bitfield
    *     The string representation of the bitfield
    *
    *  @return
    *    The symbol identified through the bitfield string, 0 if failed
    */
    static {{api.identifier}}::{{binding.bitfieldType}} getBitfield(const std::string & bitfield);
    
    /**
    *  @brief
    *    Returns the list of all bitfields known by the {{profile.inputfile}}
    *
    *  @return
    *    The list of all bitfields known by the {{profile.inputfile}}
    */
    static std::vector<{{api.identifier}}::{{binding.bitfieldType}}> bitfields();

    /**
    *  @brief
    *    Converts a {{binding.enumType}} to a string
    *
    *  @param[in] {{api.identifier}}enum
    *    The enum to convert
    *
    *  @return
    *    A string representation of the GLenum symbol name
    *
    *  @remark
    *    Beware, that some enums in the OpenGL API have different symbol names but identical enum values and that this function cannot differentiate between them
    */
    // static const std::string & getString({{api.identifier}}::{{binding.enumType}} {{api.identifier}}enum);
    
    /**
    *  @brief
    *    Converts a string to an enum symbol
    *
    *  @param[in] {{api.identifier}}enum
    *    The string representation of the enum
    *
    *  @return
    *    The symbol identified through the enum string, 0 if failed
    */
    static {{api.identifier}}::{{binding.enumType}} getEnum(const std::string & {{api.identifier}}enum);
    
    /**
    *  @brief
    *    Returns the list of all enums known by the {{profile.inputfile}}
    *
    *  @return
    *    The list of all enums known by the {{profile.inputfile}}
    */
    static std::set<{{api.identifier}}::{{binding.enumType}}> enums();

    /**
    *  @brief
    *    Converts a {{binding.booleanType}} to a string
    *
    *  @param[in] {{api.identifier}}boolean
    *    The boolean to convert
    *
    *  @return
    *    A string representation of the {{binding.booleanType}} symbol name
    *
    *  @remark
    *    Can either be `{{api.identifier|upper}}_TRUE` or `{{api.identifier|upper}}_FALSE`
    */
    static const std::string & getString(const {{api.identifier}}::{{binding.booleanType}} & {{api.identifier}}boolean);
    
    /**
    *  @brief
    *    Converts a string to a {{binding.booleanType}} symbol
    *
    *  @param[in] boolean
    *    The string representation of the {{binding.booleanType}}
    *
    *  @return
    *    The symbol identified through the boolean string, `{{api.identifier|upper}}_FALSE` if failed
    */
    static {{api.identifier}}::{{binding.booleanType}} getBoolean(const std::string & boolean);

    /**
    *  @brief
    *    Converts a {{binding.extensionType}} to its string representation
    *
    *  @param[in] {{api.identifier}}extension
    *    The extension to convert
    *
    *  @return
    *    The string representation of the extension
    */
    static const std::string & getString({{api.identifier}}::{{binding.extensionType}} {{api.identifier}}extension);
    
    /**
    *  @brief
    *    Converts a string to an {{binding.extensionType}}
    *
    *  @param[in] extension
    *    The string representation of the extension
    *
    *  @return
    *    The symbol identified through the extension string, 'UNKNOWN' if failed
    */
    static {{api.identifier}}::{{binding.extensionType}} getExtension(const std::string & extension);

    /**
    *  @brief
    *    Returns the set of all extensions known by the {{profile.inputfile}}
    *
    *  @return
    *    The set of all extensions known by the {{profile.inputfile}}
    */
    static std::set<{{api.identifier}}::{{binding.extensionType}}> extensions();
    
    /**
    *  @brief
    *    Returns the set of extensions that are required for by the given version
    *
    *  @param[in] version
    *    The version/feature to return the required extensions for.
    *    If an null version is given, all extensions that have no
    *    version/feature associated are returned instead
    *
    *  @return
    *    The set of extensions that should be supported for the given version.
    *    All non-versioned extensions can be queried by providing the null version
    */
    static const std::set<{{api.identifier}}::{{binding.extensionType}}> extensions(const Version & version);

    /**
    *  @brief
    *    Returns the list of extensions that are requiring a function
    *
    *  @param[in] function
    *    The name of the function, including the '{{api.identifier}}' prefix
    *
    *  @return
    *    The set of extensions that are requiring a function
    */
    static const std::set<{{api.identifier}}::{{binding.extensionType}}> extensions(const std::string & {{api.identifier}}function);

    /**
    *  @brief
    *    Returns the list of features that are requiring a function
    *
    *  @param[in] function
    *    The name of the function, including the '{{api.identifier}}' prefix
    *
    *  @return
    *    The set of features that are requiring a function
    */
    static const std::set<Version> versions(const std::string & {{api.identifier}}function);
    
    /**
    *  @brief
    *    Returns the set of functions that are required for the version
    *
    *  @param[in] version
    *    The version to return the required functions for
    *
    *  @return
    *    The set of functions that are required for the version
    *
    *  @remark
    *    This is exclusive (preceeding versions are ignored)
    */
    static const std::set<AbstractFunction *> functions(const Version & version);

    /**
    *  @brief
    *    Returns the set of functions that are required for the extension
    *
    *  @param[in] extension
    *    The extension to return the required functions for
    *
    *  @return
    *    The set of functions that are required for the extension
    */
    static const std::set<AbstractFunction *> functions({{api.identifier}}::{{binding.extensionType}} extension);

    /**
    *  @brief
    *    Returns the first Version (Feature) that required the extension
    *
    *  @param[in] {{api.identifier}}extension
    *    The extension
    *
    *  @return
    *    The first Version (Feature) that required the extension
    */
    static const Version & version({{api.identifier}}::{{binding.extensionType}} {{api.identifier}}extension);
    
    /**
    *  @brief
    *    Returns the list of all Versions (Features) known by the {{profile.inputfile}}
    *
    *  @return
    *    The list of all Versions (Features) known by the {{profile.inputfile}}
    */
    static const std::set<Version> & versions();
{% for group in bitfieldGroups|sort(attribute='identifier') %}
    /**
    *  @brief
    *    Convert bitfield to symbol name string representation
    *
    *  @param[in] {{api.identifierl}}bitfield
    *    The bitfield value
    *
    *  @return
    *    The string representation of the value
    */
    static const std::string & getString({{api.identifier}}::{{group.identifier}} {{api.identifier}}bitfield);
{% endfor %}
{% for group in enumGroups|sort(attribute='identifier') %}
    /**
    *  @brief
    *    Convert enum to symbol name string representation
    *
    *  @param[in] {{api.identifierl}}enum
    *    The enum value
    *
    *  @return
    *    The shortest string representation of the value
    *
    *  @remark
    *    Beware, that some enums in the API have different symbol names but identical enum values and that this function cannot differentiate between them
    */
    static const std::string & getString({{api.identifier}}::{{group.identifier}} {{api.identifier}}enum);

    /**
    *  @brief
    *    Convert enum to symbol name string representation
    *
    *  @param[in] {{api.identifierl}}enum
    *    The enum value
    *
    *  @return
    *    All string representations of the value
    */
    static std::vector<std::string> getStrings({{api.identifier}}::{{group.identifier}} {{api.identifier}}enum);
{% endfor %}

private:
    /**
    *  @brief
    *    Returns the bucket index of an identifier used for the actual lookup into the compile-time maps
    *
    *  @param[in] identifier
    *    The identifier for the bucket lookup
    *
    *  @param[in] prefixLength
    *    The length of the prefix (e.g., '{{api.identifier}}' or '{{api.identifier|upper}}_') to omit to get the actual first character of the identifier
    *
    *  @return
    *    The bucket index of an identifier
    */
    static size_t alphabeticalGroupIndex(const std::string & identifier, std::uint8_t prefixLength);
};


} } // namespace {{binding.bindingAuxNamespace}}
