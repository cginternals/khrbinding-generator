
#include <{{binding.identifier}}/{{binding.identifier}}.h>

#include <{{binding.identifier}}/AbstractFunction.h>
#include <{{binding.identifier}}/Binding.h>
#include <{{binding.identifier}}/FunctionCall.h>


namespace {{binding.namespace}}
{


void initialize({{binding.identifier}}::GetProcAddress functionPointerResolver, bool resolveFunctions) {{profile.noexceptMacro}}
{
    Binding::initialize(functionPointerResolver, resolveFunctions);
}

void initialize(ContextHandle context, {{binding.identifier}}::GetProcAddress functionPointerResolver, bool useContext, bool resolveFunctions) {{profile.noexceptMacro}}
{
    Binding::initialize(context, functionPointerResolver, useContext, resolveFunctions);
}

void useCurrentContext() {{profile.noexceptMacro}}
{
    Binding::useCurrentContext();
}

void useContext(ContextHandle context) {{profile.noexceptMacro}}
{
    Binding::useContext(context);
}

void releaseCurrentContext() {{profile.noexceptMacro}}
{
    Binding::releaseCurrentContext();
}

void releaseContext(ContextHandle context) {{profile.noexceptMacro}}
{
    Binding::releaseContext(context);
}

void registerAdditionalFunction(AbstractFunction * function) {{profile.noexceptMacro}}
{
    Binding::registerAdditionalFunction(function);
}

ProcAddress resolveFunction(const char * name) {{profile.noexceptMacro}}
{
    return Binding::resolveFunction(name);
}

void resolveFunctions() {{profile.noexceptMacro}}
{
    Binding::resolveFunctions();
}

void addContextSwitchCallback(ContextSwitchCallback callback) {{profile.noexceptMacro}}
{
    Binding::addContextSwitchCallback(callback);
}

void setCallbackMask(CallbackMask mask) {{profile.noexceptMacro}}
{
    Binding::setCallbackMask(mask);
}

void setCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList) {{profile.noexceptMacro}}
{
    Binding::setCallbackMaskExcept(mask, blackList);
}

void addCallbackMask(CallbackMask mask) {{profile.noexceptMacro}}
{
    Binding::addCallbackMask(mask);
}

void addCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList) {{profile.noexceptMacro}}
{
    Binding::addCallbackMaskExcept(mask, blackList);
}

void removeCallbackMask(CallbackMask mask) {{profile.noexceptMacro}}
{
    Binding::removeCallbackMask(mask);
}

void removeCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList) {{profile.noexceptMacro}}
{
    Binding::removeCallbackMaskExcept(mask, blackList);
}

SimpleFunctionCallback unresolvedCallback() {{profile.noexceptMacro}}
{
    return Binding::unresolvedCallback();
}

void setUnresolvedCallback(SimpleFunctionCallback callback) {{profile.noexceptMacro}}
{
    Binding::setUnresolvedCallback(callback);
}

FunctionCallback beforeCallback() {{profile.noexceptMacro}}
{
    return Binding::beforeCallback();
}

void setBeforeCallback(FunctionCallback callback) {{profile.noexceptMacro}}
{
    Binding::setBeforeCallback(callback);
}

FunctionCallback afterCallback() {{profile.noexceptMacro}}
{
    return Binding::afterCallback();
}

void setAfterCallback(FunctionCallback callback) {{profile.noexceptMacro}}
{
    Binding::setAfterCallback(callback);
}

FunctionLogCallback logCallback() {{profile.noexceptMacro}}
{
    return Binding::logCallback();
}

void setLogCallback(FunctionLogCallback callback) {{profile.noexceptMacro}}
{
    Binding::setLogCallback(callback);
}


} // namespace {{binding.namespace}}
