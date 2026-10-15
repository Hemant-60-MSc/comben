import os
import sys
# import platform
from mpi4py import MPI
from cpuInfo import CpuInfo
import wrapper

P_CORE_LINUX_FILE_PATH = '/sys/devices/cpu_core/cpus'
E_CORE_LINUX_FILE_PATH = '/sys/devices/cpu_atom/cpus'

# TODO: Set to a higher value
ITERATIONS = 1_000_000 # Leaving small for now for quick testing

def main():

    core_data={
        "TYPE": None,
        "ID": None,
        "GPU_SAMPLE_KERNEL_TIME": None,
        "CPU_TEST_FUNCION": None,
        "CPU_PTHREAD_TIME": None
    }

    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    node_name = MPI.Get_processor_name()
    time_elasped = 0.0

    core_data["ID"] = rank

    if (rank == 0):
        cpu_info = CpuInfo(P_CORE_LINUX_FILE_PATH = P_CORE_LINUX_FILE_PATH,
                        E_CORE_LINUX_FILE_PATH=E_CORE_LINUX_FILE_PATH)

        for i in range(1, size):
            core_type = {'core_type': cpu_info.classify_core_id(i)}
            comm.send(core_type, 
                      dest = i,
                      tag=i)
    
            sys.stdout.flush()

    comm.Barrier()

    gpu_time = None
    p_thread_time = None
    for curr_core in range(size):
        comm.Barrier()
        if rank == curr_core:
            gpu_time = wrapper.py_run_sample_kernel()
    comm.Barrier()

    core_data["GPU_SAMPLE_KERNEL_TIME"] = gpu_time
    core_data["CPU_PTHREAD_TIME"] = wrapper.py_pthread_measure_sample_function()

    if (rank == 0):
        core_data["TYPE"] = cpu_info.classify_core_id(rank)
    else:
        core_type = comm.recv(source = 0, tag = rank)
        core_data["TYPE"] = core_type["core_type"]

    comm.Barrier()

    for _ in range(ITERATIONS):
        time_elasped += wrapper.py_test_function()

    core_data["CPU_TEST_FUNCION"] = time_elasped

    core_datas = comm.gather(core_data, root = 0)

    if rank ==0:
        print(core_datas)

if __name__ =="__main__":
    main() 