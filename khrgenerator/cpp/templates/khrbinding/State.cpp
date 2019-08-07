
#include <{{binding.identifier}}/State.h>

#include <{{binding.identifier}}/Binding.h>


namespace {{binding.namespace}}
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


} // namespace {{binding.namespace}}
