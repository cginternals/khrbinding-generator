
#pragma once


namespace {{binding.namespace}}
{


const unsigned int {{binding.baseNamespace | upper}}_REVISION = {{api.revision}}; ///< The revision of the {{profile.inputfile}} at the time of code generation.


} // namespace {{binding.namespace}}
