
#include <{{binding.identifier}}/AbstractFunction.h>

#include <memory>
#include <set>
#include <cassert>
#include <type_traits>

#include <{{binding.identifier}}/{{binding.identifier}}_features.h>

#include <{{binding.identifier}}/AbstractState.h>

#include <{{binding.identifier}}/Binding.h>


namespace {{binding.namespace}}
{


AbstractFunction::AbstractFunction(const char * _name) {{profile.noexceptMacro}}
: m_name(_name)
{
}

AbstractFunction::~AbstractFunction() {{profile.noexceptMacro}}
{
}

void AbstractFunction::resolveAddress() {{profile.noexceptMacro}}
{
    auto & currentState = state();

    if (currentState.isInitialized())
    {
        return;
    }

    currentState.resolve(m_name);
}

const char * AbstractFunction::name() const {{profile.noexceptMacro}}
{
    return m_name;
}

bool AbstractFunction::isResolved() const {{profile.noexceptMacro}}
{
    return state().isResolved();
}

ProcAddress AbstractFunction::address() const {{profile.noexceptMacro}}
{
    if (!state().isInitialized())
    {
        const_cast<AbstractFunction*>(this)->resolveAddress();
    }

    return state().address();
}

bool AbstractFunction::isEnabled(const CallbackMask mask) const {{profile.noexceptMacro}}
{
    using callback_mask_t = std::underlying_type<CallbackMask>::type;
    
    return (static_cast<callback_mask_t>(state().callbackMask())
        & static_cast<callback_mask_t>(mask)) == static_cast<callback_mask_t>(mask);
}

bool AbstractFunction::isAnyEnabled(const CallbackMask mask) const {{profile.noexceptMacro}}
{   
    using callback_mask_t = std::underlying_type<CallbackMask>::type;
    
    return (static_cast<callback_mask_t>(state().callbackMask())
        & static_cast<callback_mask_t>(mask)) != 0;
}

CallbackMask AbstractFunction::callbackMask() const {{profile.noexceptMacro}}
{
    return state().callbackMask();
}

void AbstractFunction::setCallbackMask(const CallbackMask mask) {{profile.noexceptMacro}}
{
    state().setCallbackMask(mask);
}

void AbstractFunction::addCallbackMask(const CallbackMask mask) {{profile.noexceptMacro}}
{
    state().setCallbackMask(state().callbackMask() | mask);
}

void AbstractFunction::removeCallbackMask(const CallbackMask mask) {{profile.noexceptMacro}}
{
    state().setCallbackMask(state().callbackMask() & ~mask);
}

void AbstractFunction::unresolved(const AbstractFunction * function) {{profile.noexceptMacro}}
{
    Binding::unresolved(function);
}

void AbstractFunction::before(const FunctionCall & call) {{profile.noexceptMacro}}
{
    Binding::before(call);
}

void AbstractFunction::after(const FunctionCall & call) {{profile.noexceptMacro}}
{
    Binding::after(call);
}

void AbstractFunction::log(FunctionCall && call) {{profile.noexceptMacro}}
{
    Binding::log(std::move(call));
}

int AbstractFunction::currentPos() {{profile.noexceptMacro}}
{
    return Binding::currentPos();
}

int AbstractFunction::maxPos() {{profile.noexceptMacro}}
{
    return Binding::maxPos();
}


} // namespace {{binding.namespace}}
