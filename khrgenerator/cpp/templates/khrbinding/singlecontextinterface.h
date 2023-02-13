
#pragma once


#include <set>
#include <vector>
#include <functional>
#include <string>

#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>

#include <{{binding.identifier}}/CallbackMask.h>
#include <{{binding.identifier}}/ProcAddress.h>


namespace {{binding.namespace}}
{


class AbstractFunction;
class FunctionCall;


using SimpleFunctionCallback = std::function<void(const AbstractFunction &)>;
using FunctionCallback = std::function<void(const FunctionCall &)>;
using FunctionLogCallback = std::function<void(FunctionCall &&)>;

{{binding.apiExport}} void initialize({{binding.identifier}}::GetProcAddress functionPointerResolver, bool resolveFunctions = true);
{{binding.apiExport}} void registerAdditionalFunction(AbstractFunction * function);
{{binding.apiExport}} ProcAddress resolveFunction(const char * name);
{{binding.apiExport}} void resolveFunctions();

{{binding.apiExport}} void setCallbackMask(CallbackMask mask);
{{binding.apiExport}} void setCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList);
{{binding.apiExport}} void addCallbackMask(CallbackMask mask);
{{binding.apiExport}} void addCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList);
{{binding.apiExport}} void removeCallbackMask(CallbackMask mask);
{{binding.apiExport}} void removeCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList);
{{binding.apiExport}} SimpleFunctionCallback unresolvedCallback();
{{binding.apiExport}} void setUnresolvedCallback(SimpleFunctionCallback callback);
{{binding.apiExport}} FunctionCallback beforeCallback();
{{binding.apiExport}} void setBeforeCallback(FunctionCallback callback);
{{binding.apiExport}} FunctionCallback afterCallback();
{{binding.apiExport}} void setAfterCallback(FunctionCallback callback);
{{binding.apiExport}} FunctionLogCallback logCallback();
{{binding.apiExport}} void setLogCallback(FunctionLogCallback callback);


} // namespace {{binding.namespace}}
