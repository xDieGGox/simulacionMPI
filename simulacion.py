from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
name = MPI.Get_processor_name()

print(f"Hola desde el proceso {rank} en {name}")
