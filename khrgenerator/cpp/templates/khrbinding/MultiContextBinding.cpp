
#include <{{binding.identifier}}/Binding.h>

#include <cassert>
#include <iostream>

#include <{{binding.identifier}}/State.h>
#include <{{binding.identifier}}/AbstractFunction.h>
#include <{{binding.identifier}}/getProcAddress.h>


namespace {{binding.namespace}}
{


void Binding::setCallbackMask(const CallbackMask mask) {{profile.noexceptMacro}}
{
    for (auto function : Binding::functions())
    {
        function->setCallbackMask(mask);
    }
}

void Binding::setCallbackMaskExcept(const CallbackMask mask, const std::set<std::string> & blackList) {{profile.noexceptMacro}}
{
    for (auto function : Binding::functions())
    {
        if (blackList.find(function->name()) == blackList.end())
        {
            function->setCallbackMask(mask);
        }
    }
}

void Binding::addCallbackMask(const CallbackMask mask) {{profile.noexceptMacro}}
{
    for (auto function : Binding::functions())
    {
        function->addCallbackMask(mask);
    }
}

void Binding::addCallbackMaskExcept(const CallbackMask mask, const std::set<std::string> & blackList) {{profile.noexceptMacro}}
{
    for (auto function : Binding::functions())
    {
        if (blackList.find(function->name()) == blackList.end())
        {
            function->addCallbackMask(mask);
        }
    }
}

void Binding::removeCallbackMask(const CallbackMask mask) {{profile.noexceptMacro}}
{
    for (auto function : Binding::functions())
    {
        function->removeCallbackMask(mask);
    }
}

void Binding::removeCallbackMaskExcept(const CallbackMask mask, const std::set<std::string> & blackList) {{profile.noexceptMacro}}
{
    for (auto function : Binding::functions())
    {
        if (blackList.find(function->name()) == blackList.end())
        {
            function->removeCallbackMask(mask);
        }
    }
}

Binding::SimpleFunctionCallback Binding::unresolvedCallback() {{profile.noexceptMacro}}
{
    return s_unresolvedCallback();
}

void Binding::setUnresolvedCallback(SimpleFunctionCallback callback) {{profile.noexceptMacro}}
{
    s_unresolvedCallback() = std::move(callback);
}

Binding::FunctionCallback Binding::beforeCallback() {{profile.noexceptMacro}}
{
    return s_beforeCallback();
}

void Binding::setBeforeCallback(FunctionCallback callback) {{profile.noexceptMacro}}
{
    s_beforeCallback() = std::move(callback);
}

Binding::FunctionCallback Binding::afterCallback() {{profile.noexceptMacro}}
{
    return s_afterCallback();
}

void Binding::setAfterCallback(FunctionCallback callback) {{profile.noexceptMacro}}
{
    s_afterCallback() = std::move(callback);
}

Binding::FunctionLogCallback Binding::logCallback() {{profile.noexceptMacro}}
{
    return s_logCallback();
}

void Binding::setLogCallback(Binding::FunctionLogCallback callback) {{profile.noexceptMacro}}
{
    s_logCallback() = std::move(callback);
}

void Binding::unresolved(const AbstractFunction * function) {{profile.noexceptMacro}}
{
    if (s_unresolvedCallback())
    {
        s_unresolvedCallback()(*function);
    }
}

void Binding::before(const FunctionCall & call) {{profile.noexceptMacro}}
{
    if (s_beforeCallback())
    {
        s_beforeCallback()(call);
    }
}

void Binding::after(const FunctionCall & call) {{profile.noexceptMacro}}
{
    if (s_afterCallback())
    {
        s_afterCallback()(call);
    }
}

void Binding::log(FunctionCall && call) {{profile.noexceptMacro}}
{
    if (s_logCallback())
    {
        s_logCallback()(new FunctionCall(std::move(call)));
    }
}

const std::vector<AbstractFunction *> & Binding::additionalFunctions() {{profile.noexceptMacro}}
{
    return s_additionalFunctions();
}

size_t Binding::size() {{profile.noexceptMacro}}
{
    return Binding::functions().size() + s_additionalFunctions().size();
}

void Binding::initialize(const {{binding.identifier}}::GetProcAddress functionPointerResolver, const bool resolveFunctions) {{profile.noexceptMacro}}
{
    initialize(0, functionPointerResolver, true, resolveFunctions);
}

void Binding::initialize(
    const ContextHandle context
,   const {{binding.identifier}}::GetProcAddress functionPointerResolver
,   const bool _useContext
,   const bool _resolveFunctions) {{profile.noexceptMacro}}
{
    const auto resolveWOUse = !_useContext && _resolveFunctions;
    const auto currentContext = resolveWOUse ? s_context() : static_cast<ContextHandle>(0);

    {
        std_boost::lock_guard<std_boost::recursive_mutex> lock(s_mutex());

        if (s_firstGetProcAddress() == nullptr)
        {
            s_firstGetProcAddress() = functionPointerResolver == nullptr
                ? {{binding.identifier}}::getProcAddress
                : functionPointerResolver;
        }

        s_getProcAddress() = functionPointerResolver == nullptr ? s_firstGetProcAddress() : functionPointerResolver;

        if (s_bindings().find(context) != s_bindings().cend())
        {
            return;
        }

        const auto pos = static_cast<int>(s_bindings().size());

        s_bindings()[context] = pos;

        provideState(pos);

        if(_useContext)
        {
            useContext(context);
        }

        if (_resolveFunctions)
        {
            resolveFunctions();
        }
    }

    // restore previous context
    if(resolveWOUse)
    {
        useContext(currentContext);
    }
}

ProcAddress Binding::resolveFunction(const char * name) {{profile.noexceptMacro}}
{
    if (s_getProcAddress() != nullptr)
    {
        return s_getProcAddress()(name);
    }

    if (s_firstGetProcAddress() != nullptr)
    {
        return s_firstGetProcAddress()(name);
    }

    return nullptr;
}

void Binding::registerAdditionalFunction(AbstractFunction * function) {{profile.noexceptMacro}}
{
    s_additionalFunctions().push_back(function);
}

void Binding::resolveFunctions() {{profile.noexceptMacro}}
{
    for (auto function : Binding::functions())
    {
        function->resolveAddress();
    }

    for (auto function : Binding::additionalFunctions())
    {
        function->resolveAddress();
    }
}

void Binding::useCurrentContext() {{profile.noexceptMacro}}
{
    useContext(0);
}

void Binding::useContext(const ContextHandle context) {{profile.noexceptMacro}}
{
    std_boost::lock_guard<std_boost::recursive_mutex> lock(s_mutex());

    s_context() = context;

    if (s_bindings().find(s_context()) == s_bindings().cend())
    {
        initialize(s_context(), nullptr);

        return;
    }

    setStatePos(s_bindings()[s_context()]);

    for (const auto & callback : s_contextSwitchCallbacks())
    {
        callback(s_context());
    }
}

void Binding::releaseCurrentContext() {{profile.noexceptMacro}}
{
    releaseContext(0);
}

void Binding::releaseContext(const ContextHandle context) {{profile.noexceptMacro}}
{
    std_boost::lock_guard<std_boost::recursive_mutex> lock(s_mutex());

    neglectState(s_bindings()[context]);

    s_bindings().erase(context);
}

void Binding::addContextSwitchCallback(const ContextSwitchCallback callback) {{profile.noexceptMacro}}
{
    std_boost::lock_guard<std_boost::recursive_mutex> lock(s_mutex());

    s_contextSwitchCallbacks().push_back(std::move(callback));
}

int Binding::currentPos() {{profile.noexceptMacro}}
{
    return s_pos();
}

int Binding::maxPos() {{profile.noexceptMacro}}
{
    return s_maxPos();
}

void Binding::provideState(const int pos) {{profile.noexceptMacro}}
{
    assert(pos > -1);

    // if a state at pos exists, it is assumed to be neglected before
    if (s_maxPos() < pos)
    {
        for (AbstractFunction * function : Binding::functions())
        {
            function->resizeStates(pos + 1);
        }

        s_maxPos() = pos;
    }
}

void Binding::neglectState(const int p) {{profile.noexceptMacro}}
{
    assert(p <= s_maxPos());
    assert(p > -1);

    if (p == s_maxPos())
    {
        for (AbstractFunction * function : Binding::functions())
        {
            function->resizeStates(std::max(0, p - 1));
        }

        --s_maxPos();
    }
    else
    {
        for (AbstractFunction * function : Binding::functions())
        {
            function->state(p) = State();
        }
    }

    if (p == s_pos())
    {
        s_pos() = -1;
    }
}

void Binding::setStatePos(const int p) {{profile.noexceptMacro}}
{
    s_pos() = p;
}

int & Binding::s_maxPos() {{profile.noexceptMacro}}
{
    static int maxPos = -1;

    return maxPos;
}

const Binding::array_t & Binding::functions() {{profile.noexceptMacro}}
{
    return s_functions;
}

std::vector<AbstractFunction *> & Binding::s_additionalFunctions() {{profile.noexceptMacro}}
{
    static std::vector<AbstractFunction *> additionalFunctions;

    return additionalFunctions;
}

std::vector<Binding::ContextSwitchCallback> & Binding::s_contextSwitchCallbacks() {{profile.noexceptMacro}}
{
    static std::vector<ContextSwitchCallback> callbacks;

    return callbacks;
}

Binding::SimpleFunctionCallback & Binding::s_unresolvedCallback() {{profile.noexceptMacro}}
{
    static SimpleFunctionCallback unresolvedCallback;

    return unresolvedCallback;
}

Binding::FunctionCallback & Binding::s_beforeCallback() {{profile.noexceptMacro}}
{
    static FunctionCallback beforeCallback;

    return beforeCallback;
}

Binding::FunctionCallback & Binding::s_afterCallback() {{profile.noexceptMacro}}
{
    static FunctionCallback afterCallback;

    return afterCallback;
}

Binding::FunctionLogCallback & Binding::s_logCallback() {{profile.noexceptMacro}}
{
    static FunctionLogCallback logCallback;

    return logCallback;
}

int & Binding::s_pos() {{profile.noexceptMacro}}
{
    {{binding.threadlocal}} int pos = 0;
    //static int pos = 0;

    return pos;
}

ContextHandle & Binding::s_context() {{profile.noexceptMacro}}
{
    {{binding.threadlocal}} ContextHandle context = 0;
    //static ContextHandle context = 0;

    return context;
}

{{binding.identifier}}::GetProcAddress & Binding::s_getProcAddress() {{profile.noexceptMacro}}
{
    {{binding.threadlocal}} {{binding.identifier}}::GetProcAddress getProcAddress = nullptr;
    //static {{binding.identifier}}::GetProcAddress getProcAddress = nullptr;

    return getProcAddress;
}

std_boost::recursive_mutex & Binding::s_mutex() {{profile.noexceptMacro}}
{
    static std_boost::recursive_mutex mutex;

    return mutex;
}

std::unordered_map<ContextHandle, int> & Binding::s_bindings() {{profile.noexceptMacro}}
{
    static std::unordered_map<ContextHandle, int> bindings;

    return bindings;
}

{{binding.identifier}}::GetProcAddress & Binding::s_firstGetProcAddress() {{profile.noexceptMacro}}
{
    static {{binding.identifier}}::GetProcAddress getProcAddress = nullptr;

    return getProcAddress;
}


} // namespace {{binding.namespace}}
