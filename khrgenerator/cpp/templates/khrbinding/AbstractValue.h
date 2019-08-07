
#pragma once


#include <{{api.identifier}}binding/{{api.identifier}}binding_api.h>


namespace {{api.identifier}}binding
{


/**
*  @brief
*    The AbstractValue class represents the superclass of a printable wrapper around a data type.
*
*    This class and its subclasses Value<T> are mainly used when callbacks of functions are used.
*/
class {{api.identifier|upper}}BINDING_API AbstractValue
{
public:
    /**
    *  @brief
    *    Constructor
    */
    AbstractValue();

    /**
    *  @brief
    *    Destructor for correct memory deallocation on subclasses
    */
    virtual ~AbstractValue();
};


} // namespace {{api.identifier}}binding
