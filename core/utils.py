import datetime
import socket
from mpi4py import MPI

def log(msg, tipo="LOG"):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    hostname = socket.gethostname()
    rank = MPI.COMM_WORLD.Get_rank()
    print(f"[{tipo}][{now}][RANK {rank}][{hostname}] {msg}")

    with open(f"log_{hostname}_rank{rank}.txt", "a") as f:
        f.write(f"[{tipo}][{now}][RANK {rank}][{hostname}] {msg}\n")