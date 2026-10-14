clean:
    rm -rf build
    rm -rf wrapper*.so

compilec:
    gcc -fPIC -shared -o test_function.so test_function.c

wrap:
    python3 setup.py build_ext --inplace

compile-cuda:
    nvcc cuda_test.cu -o cuda_test

compile-cuda-lib:
    nvcc -c -Xcompiler -fPIC cuda_test.cu -o cuda_test.o

run-multi:
    mpirun -n $(grep -c ^processor /proc/cpuinfo)  --bind-to core python3 comben_main.py