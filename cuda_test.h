
#define CUDA_ARRAY_SIZE 5'000'000
#define GPU_ITERATIONS 1000
#define THREADS_PER_BLOCK 256

__global__ void sample_kernel();
#ifdef __cplusplus
extern "C"
{
#endif
    float run_sample_kernel();
#ifdef __cplusplus
}
#endif