from mpi4py import MPI
from multiprocessing import Manager
from core.vehiculo import Vehiculo
from core.utils import log
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank != 0:
    exit()

vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]

manager = Manager()
estados = manager.dict({via: "rojo" for via in vias})
vehiculos = []

log("Iniciando nodo de vehículos", "VEHICULOS")

# Lanzar algunos vehículos por vía
for via in vias:
    for i in range(2):
        v = Vehiculo(f"{via}-{i}", via, estados)
        v.start()
        vehiculos.append(v)

# Escuchar los estados de semáforos
while True:
    data = comm.recv(source=1, tag=11)
    via, nuevo_estado = data
    estados[via] = nuevo_estado
    comm.send(("vehiculo", via, nuevo_estado), dest=2, tag=20)
