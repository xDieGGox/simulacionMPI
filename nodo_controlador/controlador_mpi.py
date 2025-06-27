from mpi4py import MPI
from core.utils import log
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank != 1:
    exit()

vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]
grupos = [["Norte->Sur", "Sur->Norte"], ["Este->Oeste", "Oeste->Este"]]
estados = {via: "rojo" for via in vias}

log("Iniciando nodo controlador", "CONTROLADOR")

while True:
    for grupo in grupos:
        for via in grupo:
            estados[via] = "verde"
            comm.send((via, "verde"), dest=0, tag=11)
            comm.send((via, "verde"), dest=2, tag=12)
        time.sleep(4)

        for via in grupo:
            estados[via] = "amarillo"
            comm.send((via, "amarillo"), dest=0, tag=11)
            comm.send((via, "amarillo"), dest=2, tag=12)
        time.sleep(2)

        for via in grupo:
            estados[via] = "rojo"
            comm.send((via, "rojo"), dest=0, tag=11)
            comm.send((via, "rojo"), dest=2, tag=12)
