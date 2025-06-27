from mpi4py import MPI
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.utils import log
import socket

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
hostname = socket.gethostname()

print(f"[RANK {rank} en {hostname}] Proceso iniciado correctamente.")
log(f"Proceso controlador activo en {hostname} con rank {rank}", "CONTROLADOR")


from core.tklog import LogWindow
log_window = LogWindow("Controlador MPI")

log_window.write(f"Controlador activo en {hostname} con rank {rank}")





if rank != 1:
    exit()

vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]
grupos = [["Norte->Sur", "Sur->Norte"], ["Este->Oeste", "Oeste->Este"]]
estados = {via: "rojo" for via in vias}

log("Iniciando nodo controlador", "CONTROLADOR")

while True:
    for grupo in grupos:
        # Luz verde
        for via in grupo:
            estados[via] = "verde"
            comm.send(("vehiculo", via, "verde"), dest=0, tag=11)  # Nodo vehículos
            comm.send(("semaforo", via, "verde"), dest=2, tag=12)  # Nodo GUI
        time.sleep(4)

        # Luz amarilla
        for via in grupo:
            estados[via] = "amarillo"
            comm.send(("vehiculo", via, "amarillo"), dest=0, tag=11)
            comm.send(("semaforo", via, "amarillo"), dest=2, tag=12)
        time.sleep(1)

        # Luz roja
        for via in grupo:
            estados[via] = "rojo"
            comm.send(("vehiculo", via, "rojo"), dest=0, tag=11)
            comm.send(("semaforo", via, "rojo"), dest=2, tag=12)
