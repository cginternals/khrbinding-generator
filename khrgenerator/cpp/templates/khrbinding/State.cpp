
#include <{{api.identifier}}binding/State.h>

#include <{{api.identifier}}binding/Binding.h>


namespace {{api.identifier}}binding
{


void State::resolve(const char * name)
{
    if (m_initialized)
    {
        return;
    }

    m_address = Binding::resolveFunction(name);
    m_initialized = true;
}


} // namespace {{api.identifier}}binding
