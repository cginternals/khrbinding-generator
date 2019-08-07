
#pragma once


#include <functional>

#include <{{binding.identifier}}/{{binding.identifier}}_api.h>


namespace {{binding.namespace}}
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


} // namespace {{binding.namespace}}
