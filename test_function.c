#include "test_function.h"
#include <time.h>
#include <pthread.h>

/*************************************
 * HELPER FUNCTION(S) DECLARATION(S)
 ************************************/
void *pthread_sample_function();

/*************************************
 * PYTHON INTERFACED/CALLABLE FUNTIONS
 ************************************/
float test_function()
{
    clock_t start_time = clock();
    long long a = 1;
    for (int i = 0; i < LARGE_ITERATION_BOUND; i++)
    {
        a *= a;
    }
    clock_t end_time = clock();

    return (float)(end_time - start_time) / CLOCKS_PER_SEC;
}

float pthread_measure_sample_function()
{
    clock_t start_time = clock();
    pthread_t threads[MAX_THREADS_PER_CORE];
    int thread_exit_code;

    for (int i = 0; i < MAX_THREADS_PER_CORE; i++)
    {
        thread_exit_code = pthread_create(&threads[i], NULL, pthread_sample_function, NULL);
        if (thread_exit_code)
        {
            return -1.0;
        }
    }

    for (int i = 0; i < MAX_THREADS_PER_CORE; i++)
    {
        pthread_join(threads[i], NULL);
    }
    clock_t end_time = clock();

    return (float)(end_time - start_time) / CLOCKS_PER_SEC;
}

/*************************************
 * HELPER FUNCTION(S) DEFINTION(S)
 ************************************/

void *pthread_sample_function()
{
    long long some_num = 127;
    for (int i = 0; i < LARGE_ITERATION_BOUND; i++)
    {
        some_num *= some_num;
    }
    pthread_exit(NULL);
}