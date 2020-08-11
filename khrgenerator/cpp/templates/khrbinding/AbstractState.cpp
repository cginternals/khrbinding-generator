
#include <{{binding.identifier}}/AbstractState.h>

namespace {{binding.namespace}}
{

AbstractState::AbstractState() {{profile.noexceptMacro}}
: m_address(nullptr)
, m_initialized(false)
, m_callbackMask(CallbackMask::None)
{
}

AbstractState::~AbstractState() {{profile.noexceptMacro}}
{
}

ProcAddress AbstractState::address() const {{profile.noexceptMacro}}
{
    if (!m_initialized)
    {
        return nullptr;
    }

    return m_address;
}

bool AbstractState::isInitialized() const {{profile.noexceptMacro}}
{
    return m_initialized;
}

bool AbstractState::isResolved() const {{profile.noexceptMacro}}
{
    return m_address != nullptr;
}

CallbackMask AbstractState::callbackMask() const {{profile.noexceptMacro}}
{
    return m_callbackMask;
}

void AbstractState::setCallbackMask(CallbackMask mask) {{profile.noexceptMacro}}
{
    m_callbackMask = mask;
}

} // namespace {{binding.namespace}}
