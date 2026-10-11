import os
from setuptools import setup, Extension
from Cython.Build import cythonize

CUDA_HOME = os.environ.get("CUDA_HOME", "/usr/lib/cuda")


ext = Extension(
    "wrapper",
    sources=["wrapper.pyx", "test_function.c"],
    extra_objects=["cuda_test.o"],                      
    libraries=["cudart"],
    extra_link_args=["-lstdc++"],                       
)

setup(ext_modules=cythonize(ext))