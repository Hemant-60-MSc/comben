#include "test_function.h"
#include <time.h>

float test_function()
{
    clock_t start_time = clock();
    long long a = 1;
    for (int i = 0; i < 1000000000; i++)
    {
        a *= a;
    }
    clock_t end_time = clock();

    return (float)(end_time - start_time) / CLOCKS_PER_SEC;
}