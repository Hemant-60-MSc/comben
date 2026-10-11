# Declare the C function signatures from the header

cdef extern from *:
    """
    #ifdef __cplusplus
    extern "C" {
    #endif
    float run_sample_kernel();
    #ifdef __cplusplus
    }
    #endif
    """
    float run_sample_kernel()


cdef extern from "test_function.h":
    float test_function()

# Expose a Python-callable function
def py_test_function() -> float:
    return test_function()

def py_run_sample_kernel() -> float:
    return run_sample_kernel()