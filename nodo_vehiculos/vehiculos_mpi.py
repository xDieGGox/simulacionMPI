from mpi4py import MPI
import threading
import sys
import os
import time
import socket

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.vehiculo import Vehiculo
from core.utils import log
from core.tklog import LogWindow

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
hostname = socket.gethostname()


if rank != 0:
    exit()


# Logs iniciales
print(f"[RANK {rank} en {hostname}] Proceso iniciado correctamente.")
log(f"Proceso de vehículos ejecutándose en {hostname} con rank {rank}", "VEHICULOS")

# Ventana de log local
log_window = LogWindow(f"Vehículos - {hostname}")
log_window.write(f"[VEHICULOS][{hostname}][RANK {rank}] Proceso iniciado.")



vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]

# Diccionario normal para hilos
estados = {via: "rojo" for via in vias}
vehiculos = []

log("Iniciando nodo de vehículos", "VEHICULOS")

# Lanzar 3 vehículos por vía (usando Thread, no Process)
for via in vias:
    for i in range(3):
        v = Vehiculo(f"{via}-{i}", via, estados)
        v.start()
        vehiculos.append(v)

# Hilo para recibir los mensajes del controlador y actualizar estado
def recibir_semaforos():
    while True:
        tipo, via, nuevo_estado = comm.recv(source=1, tag=11)
        estados[via] = nuevo_estado

        # Traducimos para GUI
        if nuevo_estado == "verde":
            estado_vehiculo = "avanzando"
        elif nuevo_estado == "amarillo":
            estado_vehiculo = "desacelerando"
        else:
            estado_vehiculo = "detenido"

        comm.send(("vehiculo", via, estado_vehiculo), dest=2, tag=20)
        log_window.write(f"Semáforo {via} → {nuevo_estado.upper()} → Vehículo {estado_vehiculo.upper()}")


# Ejecutar la recepción en un hilo
thread = threading.Thread(target=recibir_semaforos, daemon=True)
thread.start()

# Iniciar GUI y mantenerla viva
log_window.start()

# Mantener el proceso vivo
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Cerrando nodo de vehículos.")
