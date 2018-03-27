
#include <{{binding}}/{{binding}}.h>

#include <{{binding}}/AbstractFunction.h>
#include <{{binding}}/Binding.h>
#include <{{binding}}/FunctionCall.h>


namespace {{binding}}
{


void initialize({{binding}}::GetProcAddress functionPointerResolver, bool resolveFunctions)
{
    Binding::initialize(functionPointerResolver, resolveFunctions);
}

void registerAdditionalFunction(AbstractFunction * function)
{
    Binding::registerAdditionalFunction(function);
}

ProcAddress resolveFunction(const char * name)
{
    return Binding::resolveFunction(name);
}

void resolveFunctions()
{
    Binding::resolveFunctions();
}

void addContextSwitchCallback(ContextSwitchCallback callback)
{
    Binding::addContextSwitchCallback(callback);
}

void setCallbackMask(CallbackMask mask)
{
    Binding::setCallbackMask(mask);
}

void setCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList)
{
    Binding::setCallbackMaskExcept(mask, blackList);
}

void addCallbackMask(CallbackMask mask)
{
    Binding::addCallbackMask(mask);
}

void addCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList)
{
    Binding::addCallbackMaskExcept(mask, blackList);
}

void removeCallbackMask(CallbackMask mask)
{
    Binding::removeCallbackMask(mask);
}

void removeCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList)
{
    Binding::removeCallbackMaskExcept(mask, blackList);
}

SimpleFunctionCallback unresolvedCallback()
{
    return Binding::unresolvedCallback();
}

void setUnresolvedCallback(SimpleFunctionCallback callback)
{
    Binding::setUnresolvedCallback(callback);
}

FunctionCallback beforeCallback()
{
    return Binding::beforeCallback();
}

void setBeforeCallback(FunctionCallback callback)
{
    Binding::setBeforeCallback(callback);
}

FunctionCallback afterCallback()
{
    return Binding::afterCallback();
}

void setAfterCallback(FunctionCallback callback)
{
    Binding::setAfterCallback(callback);
}

FunctionLogCallback logCallback()
{
    return Binding::logCallback();
}

void setLogCallback(FunctionLogCallback callback)
{
    Binding::setLogCallback(callback);
}


} // namespace {{binding}}
