
#pragma once


#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>


namespace {{binding.namespace}}
{


/**
*  @brief
*    The AbstractValue class represents the superclass of a printable wrapper around a data type.
*
*    This class and its subclasses Value<T> are mainly used when callbacks of functions are used.
*/
class {{binding.apiExport}} AbstractValue
{
public:
    /**
    *  @brief
    *    Constructor
    */
    AbstractValue() {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Destructor for correct memory deallocation on subclasses
    */
    virtual ~AbstractValue() {{profile.noexceptMacro}};
};


} // namespace {{binding.namespace}}
