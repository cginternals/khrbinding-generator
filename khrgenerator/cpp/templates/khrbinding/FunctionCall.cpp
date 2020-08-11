
#include <{{binding.identifier}}/FunctionCall.h>

#include <{{binding.identifier}}/AbstractFunction.h>
#include <{{binding.identifier}}/AbstractValue.h>
#include <{{binding.identifier}}/CallbackMask.h>


namespace {{binding.namespace}}
{


FunctionCall::FunctionCall(const AbstractFunction * _function) {{profile.noexceptMacro}}
: function(_function)
, returnValue(nullptr)
{
    if (function->isAnyEnabled(CallbackMask::Timestamp))
    {
        timestamp = std::chrono::system_clock::now();
    }
}

FunctionCall::FunctionCall(FunctionCall && other) {{profile.noexceptMacro}}
: function(std::move(other.function))
, timestamp(std::move(other.timestamp))
, parameters(std::move(other.parameters))
, returnValue(std::move(other.returnValue))
{
}

FunctionCall::~FunctionCall() {{profile.noexceptMacro}}
{
}

FunctionCall & FunctionCall::operator=(FunctionCall && other) {{profile.noexceptMacro}}
{
    function = std::move(other.function);
    timestamp = std::move(other.timestamp);
    parameters = std::move(other.parameters);
    returnValue = std::move(other.returnValue);

    return *this;
}


} // namespace {{binding.namespace}}
