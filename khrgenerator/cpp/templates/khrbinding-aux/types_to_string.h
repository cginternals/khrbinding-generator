
#pragma once


#include <string>
#include <iosfwd>

#include <{{binding.bindingAuxIdentifier}}/{{binding.bindingAuxIdentifier}}_api.h>
#include <{{binding.bindingAuxIdentifier}}/{{binding.bindingAuxIdentifier}}_features.h>

#include <{{binding.identifier}}/{{api.identifier}}/types.h>
#include <{{binding.identifier}}/Value.h>


namespace {{api.identifier}}
{


{% for group in enumerators|sort(attribute='identifier') -%}
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const {{group.identifier}} & value);
{% endfor -%}
{% for group in bitfields|sort(attribute='identifier') -%}
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const {{group.identifier}} & value);
{% endfor %}

} // namespace {{api.identifier}}


namespace {{binding.namespace}}
{


class Version;


/**
*  @brief
*    Generic ostream operator for the Value template
*/
template <typename T>
{{binding.auxApiTemplateExport}} std::ostream & operator<<(std::ostream & stream, const Value<T> & value);

/**
*  @brief
*    Generic ostream operator for the Value template with pointer types
*/
template <typename T>
{{binding.auxApiTemplateExport}} std::ostream & operator<<(std::ostream & stream, const Value<T *> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLenum Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::{{binding.enumType}}> & value);

/* <- ToDo: Add back second * when implementing this function again
*  @brief
*    A specialized ostream operator for the gl::GLbitfield Value template
*/
/*template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::{{binding.bitfieldType}}> & value);*/

/**
*  @brief
*    A specialized ostream operator for the gl::GLenum Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::{{binding.booleanType}}> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLubyte * Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::GLubyte *> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLchar * Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::GLchar *> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLuint_array_2 Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifier}}::GLuint_array_2> & value);

/**
*  @brief
*    The operator to allow Versions to be printed onto a std::ostream
*/
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Version & version);

/**
*  @brief
*    The operator to allow AbstractValues to be printed onto a std::ostream
*/
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const AbstractValue * value);


} // namespace {{binding.namespace}}


#include <{{binding.bindingAuxIdentifier}}/types_to_string.inl>
