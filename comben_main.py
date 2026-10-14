import os
import sys
# import platform
from mpi4py import MPI
from cpuInfo import CpuInfo
import wrapper

P_CORE_LINUX_FILE_PATH = '/sys/devices/cpu_core/cpus'
E_CORE_LINUX_FILE_PATH = '/sys/devices/cpu_atom/cpus'

# TODO: Set tot a higher value
ITERATIONS = 1_000_000 # Leaving small for now for quick testing

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    node_name = MPI.Get_processor_name()
    time_elasped = 0.0

    if (rank == 0):
        cpu_info = CpuInfo(P_CORE_LINUX_FILE_PATH = P_CORE_LINUX_FILE_PATH,
                        E_CORE_LINUX_FILE_PATH=E_CORE_LINUX_FILE_PATH)

        for i in range(1, size):
            core_data = {'core_type': cpu_info.classify_core_id(i)}
            comm.send(core_data, 
                      dest = i,
                      tag=i)
            # print(f"Sent core type to core{i}")
            sys.stdout.flush()
    wrapper.py_run_sample_kernel()
    comm.Barrier()

    gpu_time = wrapper.py_run_sample_kernel()

    if (rank == 0):
        core_type = {'core_type': cpu_info.classify_core_id(rank)}
        # print(wrapper.py_run_sample_kernel())
        # print(f"Core {rank} is of type {core_type}, function: {wrapper.py_test_function()}")
    else:
        core_type = comm.recv(source = 0, tag = rank)
        # print(f"Core {rank} is of type {core_type['core_type']}, function: {wrapper.py_test_function()}")

    comm.Barrier()

    for _ in range(ITERATIONS):
        time_elasped += wrapper.py_test_function()

    print(f"Type: {core_type['core_type']} | Id: {rank} | time: {time_elasped} secs. | Gpu Time: {gpu_time}")

if __name__ =="__main__":
    main() 