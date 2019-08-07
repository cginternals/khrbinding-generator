
#pragma once


#include <string>
#include <iosfwd>

#include <{{api.identifier}}binding-aux/{{api.identifier}}binding-aux_api.h>
#include <{{api.identifier}}binding-aux/{{api.identifier}}binding-aux_features.h>

#include <{{api.identifier}}binding/{{api}}/types.h>
#include <{{api.identifier}}binding/Value.h>


{{#types.items}}
{{#item.integrations.streamable}}
{{#item}}{{>partials/types_streamable.h}}{{/item}}

{{/item.integrations.streamable}}
{{#item.integrations.bitfieldStreamable}}
{{#item}}{{>partials/types_bitfieldStreamable.h}}{{/item}}

{{/item.integrations.bitfieldStreamable}}
{{/types.items}}


namespace {{api.identifier}}binding
{


class Version;


template <typename T>
{{api.identifier|upper}}BINDING_AUX_TEMPLATE_API std::ostream & operator<<(std::ostream & stream, const Value<T> & value);

template <typename T>
{{api.identifier|upper}}BINDING_AUX_TEMPLATE_API std::ostream & operator<<(std::ostream & stream, const Value<T *> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLenum Value template
*/
template <>
{{api.identifier|upper}}BINDING_AUX_API std::ostream & operator<<(std::ostream & stream, const Value<{{api}}::{{enumType}}> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLbitfield Value template
*/
/*template <>
{{api.identifier|upper}}BINDING_AUX_API std::ostream & operator<<(std::ostream & stream, const Value<{{api}}::{{bitfieldType}}> & value);*/

/**
*  @brief
*    A specialized ostream operator for the gl::GLenum Value template
*/
template <>
{{api.identifier|upper}}BINDING_AUX_API std::ostream & operator<<(std::ostream & stream, const Value<{{api}}::{{booleanType}}> & value);

{{#glapi}}
/**
*  @brief
*    A specialized ostream operator for the gl::GLubyte * Value template
*/
template <>
{{api.identifier|upper}}BINDING_AUX_API std::ostream & operator<<(std::ostream & stream, const Value<{{api}}::GLubyte *> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLchar * Value template
*/
template <>
{{api.identifier|upper}}BINDING_AUX_API std::ostream & operator<<(std::ostream & stream, const Value<{{api}}::GLchar *> & value);

/**
*  @brief
*    A specialized ostream operator for the gl::GLuint_array_2 Value template
*/
template <>
{{api.identifier|upper}}BINDING_AUX_API std::ostream & operator<<(std::ostream & stream, const Value<{{api}}::GLuint_array_2> & value);
{{/glapi}}

/**
*  @brief
*    The operator to allow Versions to be printed onto a std::ostream
*/
{{api.identifier|upper}}BINDING_AUX_API std::ostream & operator<<(std::ostream & stream, const Version & version);

{{api.identifier|upper}}BINDING_AUX_API std::ostream & operator<<(std::ostream & stream, const AbstractValue * value);


} // namespace {{api.identifier}}binding


#include <{{api.identifier}}binding-aux/types_to_string.inl>
