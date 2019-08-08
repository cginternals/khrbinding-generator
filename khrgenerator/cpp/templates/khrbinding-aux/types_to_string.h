
#pragma once


#include <string>
#include <iosfwd>

#include <{{binding.identifier}}-aux/{{binding.identifier}}-aux_api.h>
#include <{{binding.identifier}}-aux/{{binding.identifier}}-aux_features.h>

#include <{{binding.identifier}}/{{api.identifer}}/types.h>
#include <{{binding.identifier}}/Value.h>


{{#types.items}}
{{#item.integrations.streamable}}
{{#item}}{{>partials/types_streamable.h}}{{/item}}

{{/item.integrations.streamable}}
{{#item.integrations.bitfieldStreamable}}
{{#item}}{{>partials/types_bitfieldStreamable.h}}{{/item}}

{{/item.integrations.bitfieldStreamable}}
{{/types.items}}


namespace {{binding.namespace}}
{


class Version;


template <typename T>
{{binding.auxApiTemplateExport}} std::ostream & operator<<(std::ostream & stream, const Value<T> & value);

template <typename T>
{{binding.auxApiTemplateExport}} std::ostream & operator<<(std::ostream & stream, const Value<T *> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLenum Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifer}}::{{enumType}}> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLbitfield Value template
*/
/*template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifer}}::{{bitfieldType}}> & value);*/

/**
*  @brief
*    A specialized ostream operator for the gl::GLenum Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifer}}::{{booleanType}}> & value);

{{#glapi}}
/**
*  @brief
*    A specialized ostream operator for the gl::GLubyte * Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifer}}::GLubyte *> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLchar * Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifer}}::GLchar *> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLuint_array_2 Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{api.identifer}}::GLuint_array_2> & value);
{{/glapi}}

/**
*  @brief
*    The operator to allow Versions to be printed onto a std::ostream
*/
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Version & version);

{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const AbstractValue * value);


} // namespace {{binding.namespace}}


#include <{{binding.identifier}}-aux/types_to_string.inl>
