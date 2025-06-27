from mpi4py import MPI
import os
import subprocess

rank = MPI.COMM_WORLD.Get_rank()

if rank == 0:
    subprocess.run(["python", "nodo_vehiculos/vehiculos_mpi.py"])
elif rank == 1:
    subprocess.run(["python", "nodo_controlador/controlador_mpi.py"])
elif rank == 2:
    subprocess.run(["python", "nodo_gui/interfaz_mpi.py"])
