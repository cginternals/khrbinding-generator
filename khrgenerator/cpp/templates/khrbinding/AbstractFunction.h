
#pragma once


#include <string>
#include <set>
#include <vector>

#include <{{binding.identifier}}/{{binding.identifier}}_api.h>

#include <{{binding.identifier}}/ProcAddress.h>
#include <{{binding.identifier}}/FunctionCall.h>
#include <{{binding.identifier}}/CallbackMask.h>


namespace {{binding.namespace}}
{


class AbstractState;
class Binding;


/**
*  @brief
*    The AbstractFunction represents an OpenGL API function by its name
*    and entry point after dynamic address resolution.
*/
class {{binding.apiExport}} AbstractFunction
{
    friend class Binding;
public:
    /**
    *  @brief
    *    Constructor
    *
    *  @param[in] name
    *    The actual exported OpenGL API function name, including the '{{api.identifier}}' prefix
    */
    AbstractFunction(const char * name) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Destructor to guarantee correct memory deallocation of subclasses
    */
    virtual ~AbstractFunction() {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Get function name
    *
    *  @return
    *    The function name
    */
    const char * name() const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Lookup the function pointer and stores it in the current state
    */
    void resolveAddress() {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Check for a valid function pointer in the current state
    *
    *  @return
    *    `true` if a valid function pointer is stored in the current state, else `false`
    */
    bool isResolved() const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Get function pointer
    *
    *  @return
    *    The function pointer
    */
    ProcAddress address() const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Get callback mask
    *
    *  @return
    *    The currently configured callback mask for the current state
    */
    CallbackMask callbackMask() const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Reconfigures the callback mask for the current state
    *
    *  @param[in] mask
    *    The new callback mask
    */
    void setCallbackMask(CallbackMask mask) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Reconfigures the callback mask for the current state in means of a bit-wise 'or' operation with the current callback mask
    *
    *  @param[in] mask
    *    The callback mask to include
    */
    void addCallbackMask(CallbackMask mask) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Reconfigures the callback mask for the current state in means of a bit-wise 'clear' operation of the current callback mask
    *
    *  @param[in] mask
    *    The callback mask to exclude
    */
    void removeCallbackMask(CallbackMask mask) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Check if all bits of the parameter are set in the currently configured callback mask of the current state
    *
    *  @param[in] mask
    *    The mask to check against
    *
    *  @return
    *    `true` if all bits are set, else `false`
    */
    bool isEnabled(CallbackMask mask) const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Check if any bit of the parameter is set in the currently configured callback mask of the current state
    *
    *  @param[in] mask
    *    The mask to check against
    *
    *  @return
    *    `true` if at least one bit is set, else `false`
    */
    bool isAnyEnabled(CallbackMask mask) const {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Resize internal cache of states
    *
    *  @param[in] count
    *    New cache size
    */
    virtual void resizeStates(int count) {{profile.noexceptMacro}} = 0;

    /**
    *  @brief
    *    Call unresolved callback
    *
    *  @param[in] function
    *    Parameter for callback
    *
    *  @see Binding::unresolvedCallback()
    */
    static void unresolved(const AbstractFunction * function) {{profile.noexceptMacro}};
    
    /**
    *  @brief
    *    Call before callback
    *
    *  @param[in] call
    *    Parameter for callback
    *
    *  @see Binding::beforeCallback()
    */
    static void before(const FunctionCall & call) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Call after callback
    *
    *  @param[in] call
    *    Parameter for callback
    *
    *  @see Binding::afterCallback()
    */
    static void after(const FunctionCall & call) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Call log callback
    *
    *  @param[in] call
    *    Parameter for callback
    *
    *  @see Binding::logCallback()
    */
    static void log(FunctionCall && call) {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Get index of current state
    *
    *  @return
    *    Index of current state
    */
    static int currentPos() {{profile.noexceptMacro}};

    /**
    *  @brief
    *    Get highest state index currently used
    *
    *  @return
    *    Highest state index currently used
    */
    static int maxPos() {{profile.noexceptMacro}};


protected:
    /**
    *  @brief
    *    Checks for existence of the current configured state
    *
    *  @return
    *    `true` if the current state still exists, else `false`
    *
    *  @remark
    *    This method is usually used to detect invalid state clean up
    */
    virtual bool hasState() const {{profile.noexceptMacro}} = 0;

    /**
    *  @brief
    *    Checks for existence of a state
    *
    *  @param[in] pos
    *    The index of the state to check
    *
    *  @return
    *    `true` if the state exists, else `false`
    */
    virtual bool hasState(int pos) const {{profile.noexceptMacro}} = 0;

    /**
    *  @brief
    *    Get current state
    *
    *  @return
    *    The current state
    */
    virtual AbstractState & state() const {{profile.noexceptMacro}} = 0;

    /**
    *  @brief
    *    Get state
    *
    *  @param[in] pos
    *    The index of the state
    *
    *  @return
    *    The state
    */
    virtual AbstractState & state(int pos) const {{profile.noexceptMacro}} = 0;


protected:
    const char * m_name; ///< The function name, including the '{{api.identifier}}' prefix
};


} // namespace {{binding.namespace}}
