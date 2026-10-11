
#include <cuda.h>
#include <cuda_runtime.h>
#include <time.h>
#include <stdio.h>
#include "cuda_test.h"

struct GPUTimingAttributes
{
    float cuda_malloc_;
    float cuda_memcpy_h2d_; // host to device
    float cuda_memcpy_d2h;  // device to host
    float cuda_free_;
} GPUTimingAttributes;

__global__ void sample_kernel()
{
    // int idx = blockDim.x * blockIdx.x + threadIdx.x;
}

extern "C" float run_sample_kernel()
{
    int numElements = CUDA_ARRAY_SIZE;
    size_t allocation_size = numElements * sizeof(float);
    float *A = (float *)malloc(allocation_size);

    // GPU Array(s)
    float *c_A = NULL;

    clock_t start_time = clock();

    for (int i = 0; i < GPU_ITERATIONS; i++)
    {
        cudaMalloc((void **)&c_A, allocation_size);
        cudaMemcpy(c_A, A, allocation_size, cudaMemcpyHostToDevice);

        int num_blocks = (numElements + THREADS_PER_BLOCK - 1) / THREADS_PER_BLOCK;
        sample_kernel<<<num_blocks, THREADS_PER_BLOCK>>>();
        cudaMemcpy(A, c_A, allocation_size, cudaMemcpyDeviceToHost);
        cudaDeviceSynchronize();

        cudaFree(c_A);
        free(A);
    }
    clock_t end_time = clock();
    cudaDeviceSynchronize();

    return (float)(end_time - start_time) / CLOCKS_PER_SEC;
}

#ifdef CUDA_TEST_STANDALONE
int main()
{

    float res = run_sample_kernel();

    printf("Time taken: %f\n sec(s)\n", res);

    return 0;
}
#endif