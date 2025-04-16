
#pragma once


#include <string>
#include <iosfwd>

#include <{{binding.bindingAuxIdentifier}}/{{binding.bindingAuxIdentifier}}_api.h>
#include <{{binding.bindingAuxIdentifier}}/{{binding.bindingAuxIdentifier}}_features.h>

#include <{{binding.identifier}}/{{binding.baseNamespace}}/types.h>
#include <{{binding.identifier}}/Value.h>


namespace {{binding.baseNamespace}}
{


{% for group in enumerators|sort(attribute='identifier') -%}
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const {{group.identifier}} & value);
{% endfor -%}
{% for group in uniqueEnumerators|sort(attribute='identifier') -%}
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const {{group.identifier}} & value);
{% endfor -%}
{% for group in bitfields|sort(attribute='identifier') -%}
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const {{group.identifier}} & value);
{% endfor %}

} // namespace {{binding.baseNamespace}}


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
*    A specialized ostream operator for the {{binding.baseNamespace}}::GLenum Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{binding.baseNamespace}}::{{binding.enumType}}> & value);

/* <- ToDo: Add back second * when implementing this function again
*  @brief
*    A specialized ostream operator for the {{binding.baseNamespace}}::GLbitfield Value template
*/
/*template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{binding.baseNamespace}}::{{binding.bitfieldType}}> & value);*/

/**
*  @brief
*    A specialized ostream operator for the {{binding.baseNamespace}}::GLenum Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{binding.baseNamespace}}::{{binding.booleanType}}> & value);

/**
*  @brief
*    A specialized ostream operator for the const char * Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<const char *> & value);

{%- for cStringTypeName in cStringTypes %}

/**
*  @brief
*    A specialized ostream operator for the {{cStringTypeName}} * Value template
*/
template <>
{{binding.auxApiExport}} std::ostream & operator<<(std::ostream & stream, const Value<{{binding.baseNamespace}}::{{cStringTypeName}} *> & value);
{%- endfor %}

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
