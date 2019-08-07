
#pragma once


#include <functional>

#include <{{api.identifier}}binding/{{api.identifier}}binding_api.h>


namespace {{api.identifier}}binding
{


/**
*  @brief
*    The generic pointer to a function
*/
using ProcAddress = void(*)();

/**
*  @brief
*    The signature for the getProcAddress function
*/
using GetProcAddress = std::function<ProcAddress(const char*)>;


} // namespace {{api.identifier}}binding
