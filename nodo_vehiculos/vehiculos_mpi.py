from mpi4py import MPI
import threading
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.vehiculo import Vehiculo
from core.utils import log

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank != 0:
    exit()

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

# Ejecutar la recepción en un hilo
thread = threading.Thread(target=recibir_semaforos, daemon=True)
thread.start()

# Mantener el proceso vivo
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Cerrando nodo de vehículos.")
