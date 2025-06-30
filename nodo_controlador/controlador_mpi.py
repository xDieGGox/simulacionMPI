from mpi4py import MPI
import sys
import threading
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.utils import log
import socket
from core.tklog import LogWindow

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
hostname = socket.gethostname()



if rank != 1:
    exit()


print(f"[RANK {rank} en {hostname}] Proceso iniciado correctamente.")
log(f"Proceso controlador activo en {hostname} con rank {rank}", "CONTROLADOR")


log_window = LogWindow(title=f"Controlador - {hostname}")
log_window.write(f"[CONTROLADOR][{hostname}][RANK {rank}] Proceso iniciado.")


vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]
grupos = [["Norte->Sur", "Sur->Norte"], ["Este->Oeste", "Oeste->Este"]]
estados = {via: "rojo" for via in vias}

log("Iniciando nodo controlador", "CONTROLADOR")


def ciclo_controlador():
    while True:
        for grupo in grupos:
            # Verde
            for via in grupo:
                estados[via] = "verde"
                comm.send(("vehiculo", via, "verde"), dest=0, tag=11)
                comm.send(("semaforo", via, "verde"), dest=2, tag=12)
                log_window.write(f"Semáforo {via} en VERDE")
            comm.bcast(estados.copy(), root=1) 
            time.sleep(4)

            # Amarillo
            for via in grupo:
                estados[via] = "amarillo"
                comm.send(("vehiculo", via, "amarillo"), dest=0, tag=11)
                comm.send(("semaforo", via, "amarillo"), dest=2, tag=12)
                log_window.write(f"Semáforo {via} en AMARILLO")
            comm.bcast(estados.copy(), root=1)
            time.sleep(1)

            # Rojo
            for via in grupo:
                estados[via] = "rojo"
                comm.send(("vehiculo", via, "rojo"), dest=0, tag=11)
                comm.send(("semaforo", via, "rojo"), dest=2, tag=12)
                log_window.write(f"Semáforo {via} en ROJO")
            comm.bcast(estados.copy(), root=1)  # Broadcast estados

# Lanzar el controlador en un hilo
controlador_thread = threading.Thread(target=ciclo_controlador, daemon=True)
controlador_thread.start()

# Mantener la GUI activa
log_window.start()