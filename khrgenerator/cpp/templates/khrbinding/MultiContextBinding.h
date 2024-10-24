
#pragma once


#include <string>
#include <set>
#include <array>
#include <vector>
#include <functional>
#include <unordered_map>

#ifdef {{binding.useboostthread}}
#include <boost/thread.hpp>
namespace std_boost = boost;
#else
#include <mutex>
namespace std_boost = std;
#endif

#include <{{binding.identifier}}/{{binding.identifier}}_api.h>
#include <{{binding.identifier}}/{{binding.identifier}}_features.h>

#include <{{binding.identifier}}/AbstractFunction.h>
#include <{{binding.identifier}}/ContextHandle.h>
#include <{{binding.identifier}}/Function.h>
#include <{{binding.identifier}}/CallbackMask.h>
#include <{{binding.identifier}}/FunctionCall.h>
#include <{{binding.identifier}}/ProcAddress.h>

#include <{{binding.identifier}}/{{binding.baseNamespace}}/types.h>


namespace {{binding.namespace}}
{


/**
*  @brief
*    The main interface to handle additional features to OpenGL functions besides regular function calls
*
*  Additional features include binding initialization (even for multi-threaded environments), additional function registration,
*  context switches (for multi-context environments) and basic reflection in form of accessors to the full list of functions.
*/
class {{binding.apiExport}} Binding
{
public:
    /**
    *  @brief
    *    The callback type of a simple function callback without parameters and return value
    */
    using SimpleFunctionCallback = std::function<void(const AbstractFunction &)>;

    /**
    *  @brief
    *    The callback type of a function callback with parameters and return value
    */
    using FunctionCallback = std::function<void(const FunctionCall &)>;

    /**
    *  @brief
    *    The callback type of a function log callback with parameters and return value
    */
    using FunctionLogCallback = std::function<void(FunctionCall &&)>;

    using ContextSwitchCallback = std::function<void(ContextHandle)>;   ///< The signature of the context switch callback
    
    using array_t = std::array<AbstractFunction *, {{functions|count}}>; ///< The type of the build-in functions collection


public:
    /**
    *  @brief
    *    Deleted Constructor as all functions are static
    */
    Binding() = delete;

    /**
    *  @brief
    *    Initializes the binding for the current active OpenGL context
    *
    *  @param[in] functionPointerResolver
    *    A function pointer to resolve binding functions for this context.
    *    If `nullptr` is passed for first time initialization, `{{binding.identifier}}::getProcAddress` is used for convenience.
    *  @param[in] resolveFunctions (optional)
    *    Whether to resolve function pointers lazy (\a resolveFunctions = `false`) or immediately
    *
    *  @remark
    *    After this call, the initialized context is already set active for the current thread.
    *
    *  @remark
    *    A functionPointerResolver with value 'nullptr' will get initialized with the function
    *    pointer from the initial thread.
    *
    *  @remark
    *    Using {{binding.identifier}}::getProcAddress is provided for convenience only. Please don't use this in new code.
    *    Instead, use an external function resolution callback, e.g.,
    *     * wglGetProcAddress
    *     * glxGetProcAddress
    *     * glfwGetProcAddress
    *     * QOpenGlContext::getProcAddress
    */
    static void initialize({{binding.identifier}}::GetProcAddress functionPointerResolver, bool resolveFunctions = true);

    /**
    *  @brief
    *    Initializes the binding for a specific OpenGL context
    *
    *  @param[in] context
    *    The context handle of the context to initialize
    *  @param[in] functionPointerResolver
    *    A function pointer to resolve binding functions for this context
    *  @param[in] useContext
    *    Whether to set the context active (\a useContext = `true`) after the initialization
    *  @param[in] resolveFunctions (optional)
    *    Whether to resolve function pointers lazy (\a resolveFunctions = `false`) or immediately
    *
    *  @remark
    *    A functionPointerResolver with value 'nullptr' will get initialized with the function
    *    pointer from the initial thread.
    */
    static void initialize(ContextHandle context, {{binding.identifier}}::GetProcAddress functionPointerResolver, bool useContext = true, bool resolveFunctions = true);

    /**
    *  @brief
    *    Registers an additional function for the additional features
    *
    *  @param[in] function
    *    The function to register
    */
    static void registerAdditionalFunction(AbstractFunction * function);

    /**
    *  @brief
    *    Resolve a single function pointer by given name
    *
    *  @param[in] name
    *    The name of the function
    */
    static ProcAddress resolveFunction(const char * name);

    /**
    *  @brief
    *    Resolves the funtion pointers of all registered OpenGL functions immediately for the current context
    */
    static void resolveFunctions();

    /**
    *  @brief
    *    Update the current context state in {{binding.identifier}}
    *
    *  @remark
    *    This function queries the driver for the current OpenGL context
    */
    static void useCurrentContext();

    /**
    *  @brief
    *    Update the current context state in {{binding.identifier}}
    *
    *  @param[in] context
    *    The context handle of the context to set current
    */
    static void useContext(ContextHandle context);

    /**
    *  @brief
    *    Removes the current context from the state of {{binding.identifier}}
    *
    *  @remark
    *    This function queries the driver for the current OpenGL context
    */
    static void releaseCurrentContext();

    /**
    *  @brief
    *    Removes the current context from the state of {{binding.identifier}}
    *
    *  @param[in] context
    *    The context handle of the context to remove
    */
    static void releaseContext(ContextHandle context);

    /**
    *  @brief
    *    Registers an additional callback that gets called each time the context is switched using the useContext method
    *
    *  @remark
    *    There may be multiple context switch callbacks registered at once
    */
    static void addContextSwitchCallback(ContextSwitchCallback callback);

    /**
    *  @brief
    *    Updates the callback mask of all registered OpenGL functions in the current state
    *
    *  @param[in] mask
    *    The new CallbackMask
    */
    static void setCallbackMask(CallbackMask mask);

    /**
    *  @brief
    *    Updates the callback mask of all registered OpenGL functions in the current state, excluding the blacklisted functions
    *
    *  @param[in] mask
    *    The new CallbackMask
    *  @param[in] blackList
    *    The blacklist of functions to exclude in this update
    */
    static void setCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList);

    /**
    *  @brief
    *    Updates the callback mask of all registered OpenGL functions in the current state to include the passed CallbackMask
    *
    *  @param[in] mask
    *    The CallbackMask to include
    */
    static void addCallbackMask(CallbackMask mask);

    /**
    *  @brief
    *    Updates the callback mask of all registered OpenGL functions in the current state to include the passed CallbackMask, excluding the blacklisted functions
    *
    *  @param[in] mask
    *    The CallbackMask to include
    *  @param[in] blackList
    *    The blacklist of functions to exclude in this update
    */
    static void addCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList);

    /**
    *  @brief
    *    Updates the callback mask of all registered OpenGL functions in the current state to exclude the passed CallbackMask
    *
    *  @param[in] mask
    *    The CallbackMask to exclude
    */
    static void removeCallbackMask(CallbackMask mask);

    /**
    *  @brief
    *    Updates the callback mask of all registered OpenGL functions in the current state to exclude the passed CallbackMask, excluding the blacklisted functions
    *
    *  @param[in] mask
    *    The CallbackMask to exclude
    *  @param[in] blackList
    *    The blacklist of functions to exclude in this update
    */
    static void removeCallbackMaskExcept(CallbackMask mask, const std::set<std::string> & blackList);

    /**
    *  @brief
    *    Unresolved callback accessor
    *
    *  @return
    *    The callback to use instead of unresolved function calls
    *
    *  @remark
    *    Keep in mind that in addition to a registered callback, the callback mask of the current Function has to include the After flag to enable the callback
    */
    static SimpleFunctionCallback unresolvedCallback();

    /**
    *  @brief
    *    Updates the unresolved callback that is called upon invocation of an OpenGL function which has no counterpart in the OpenGL driver
    *
    *  @param[in] callback
    *    The callback to use instead of unresolved function calls
    *
    *  @remark
    *    This callback is registered globally across all states.
    *  @remark
    *    Keep in mind that in addition to a registered callback, the callback mask of the current Function has to include the Unresolved flag to enable the callback
    */
    static void setUnresolvedCallback(SimpleFunctionCallback callback);

    /**
    *  @brief
    *    Before callback accessor
    *
    *  @return
    *    The callback to use before an OpenGL function call
    *
    *  @remark
    *    Keep in mind that in addition to a registered callback, the callback mask of the current Function has to include the After flag to enable the callback
    */
    static FunctionCallback beforeCallback();

    /**
    *  @brief
    *    Updates the before callback that is called before the actual OpenGL function invocation
    *
    *  @param[in] callback
    *    The callback to use before an OpenGL function call
    *
    *  @remark
    *    This callback is registered globally across all states.
    *  @remark
    *    Keep in mind that in addition to a registered callback, the callback mask of the current Function has to include the Before flag to enable the callback
    */
    static void setBeforeCallback(FunctionCallback callback);

    /**
    *  @brief
    *    After callback accessor
    *
    *  @return
    *    The callback to use after an OpenGL function call
    *
    *  @remark
    *    Keep in mind that in addition to a registered callback, the callback mask of the current Function has to include the After flag to enable the callback
    */
    static FunctionCallback afterCallback();

    /**
    *  @brief
    *    Updates the after callback that is called after the actual OpenGL function invocation
    *
    *  @param[in] callback
    *    The callback to use after an OpenGL function call
    *
    *  @remark
    *    This callback is registered globally across all states.
    *  @remark
    *    Keep in mind that in addition to a registered callback, the callback mask of the current Function has to include the After flag to enable the callback
    */
    static void setAfterCallback(FunctionCallback callback);

    /**
    *  @brief
    *    Logging callback accessor
    *
    *  @return
    *    The callback to use for logging an OpenGL function call
    *
    *  @remark
    *    Keep in mind that in addition to a registered callback, the callback mask of the current Function has to include the Logging flag to enable the callback
    */
    static FunctionLogCallback logCallback();

    /**
    *  @brief
    *    Updates the logging callback that is called to log the actual OpenGL function invocation
    *
    *  @param[in] callback
    *    The callback to use for logging an OpenGL function call
    *
    *  @remark
    *    This callback is registered globally across all states.
    *
    *  @remark
    *    Keep in mind that in addition to a registered callback, the callback mask of the current Function has to include the Logging flag to enable the callback
    */
    static void setLogCallback(FunctionLogCallback callback);
    
    /**
    *  @brief
    *    The accessor for all build-in functions
    * 
    *  @return
    *    The list of all build-in functions
    */
    static const array_t & functions();

    /**
    *  @brief
    *    Accessor for additional functions
    *
    *  @return
    *    List of additional functions
    */
    static const std::vector<AbstractFunction *> & additionalFunctions();

    /**
    *  @brief
    *    Get index of current state
    *
    *  @return
    *    Index of current state
    */
    static int currentPos();

    /**
    *  @brief
    *    Get highest state index currently used
    *
    *  @return
    *    Highest state index currently used
    */
    static int maxPos();

    /**
    *  @brief
    *    Query total number of functions
    *
    *  @return
    *    Total number of functions
    */
    static size_t size();

    /**
    *  @brief
    *    Call unresolved callback
    *
    *  @param[in] function
    *    Parameter for callback
    *
    *  @see Binding::unresolvedCallback()
    */
    static void unresolved(const AbstractFunction * function);

    /**
    *  @brief
    *    Call before callback
    *
    *  @param[in] call
    *    Parameter for callback
    *
    *  @see Binding::beforeCallback()
    */
    static void before(const FunctionCall & call);

    /**
    *  @brief
    *    Call after callback
    *
    *  @param[in] call
    *    Parameter for callback
    *
    *  @see Binding::afterCallback()
    */
    static void after(const FunctionCall & call);

    /**
    *  @brief
    *    Call log callback
    *
    *  @param[in] call
    *    Parameter for callback
    *
    *  @see Binding::logCallback()
    */
    static void log(FunctionCall && call);


public:
{%- for function in functions|sort(attribute='identifier') %}
    static Function<{{function.returnType.namespacedIdentifier}}{{ ", " if function.parameters|length > 0 }}{% for param in function.parameters %}{{ param.type.namespacedIdentifier }}{{ ", " if not loop.last }}{% endfor %}> {{function.namespaceLessIdentifier}}; ///< Wrapper for {{function.identifier}}
{%- endfor %}


protected:
    /**
    *  @brief
    *    Provide an additional State
    *
    *  @param[in] pos
    *    Index of new State
    */
    static void provideState(int pos);

    /**
    *  @brief
    *    Neglect a previously provided state
    *
    *  @param[in] pos
    *    Index of State to neglect
    */
    static void neglectState(int pos);

    /**
    *  @brief
    *    Set current State
    *
    *  @param[in] pos
    *    Index of State
    */
    static void setStatePos(int pos);


protected:
    static const array_t s_functions;                                       ///< The list of all build-in functions
    static int & s_maxPos();                                                ///< Maximum State index in use
    static std::vector<AbstractFunction *> & s_additionalFunctions();       ///< List of additional OpenGL fucntions
    static std::vector<ContextSwitchCallback> & s_contextSwitchCallbacks(); ///< List of callbacks for context switch
    static SimpleFunctionCallback & s_unresolvedCallback();                 ///< Callback for unresolved functions
    static FunctionCallback & s_beforeCallback();                           ///< Callback for before function call
    static FunctionCallback & s_afterCallback();                            ///< Callback for after function call
    static FunctionLogCallback & s_logCallback();                           ///< Callback for logging a function call
    static int & s_pos();                                                   ///< Position of current State
    static ContextHandle & s_context();                                     ///< Handle of current context
    static {{binding.identifier}}::GetProcAddress & s_getProcAddress();                  ///< Current address of function resolution method
    static std_boost::recursive_mutex & s_mutex();                          ///< Mutex
    static std::unordered_map<ContextHandle, int> & s_bindings();           ///< Map (handle->position) of initialized contexts
    static {{binding.identifier}}::GetProcAddress & s_firstGetProcAddress();             ///< First address of function resolution method
};


} // namespace {{binding.namespace}}
