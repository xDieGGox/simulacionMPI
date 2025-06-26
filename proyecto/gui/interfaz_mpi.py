# interfaz_mpi.py
from multiprocessing import Manager, Lock
import tkinter as tk
import time
from proyecto.gui.interfaz import GUI
#from interfaz import GUI 
#from proyecto.core.semaforo import Semaforo
from ..core.semaforo import Semaforo
from mpi4py import MPI
import threading

def iniciar_interfaz_semaforos(comm):
    rank = comm.Get_rank()
    assert rank == 0, "Este módulo debe ejecutarse solo en el rank 0"

    print("[Rank 0 - GUI] Iniciando interfaz con semáforos...")

    vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]

    manager = Manager()
    estados = manager.dict({via: "rojo" for via in vias})
    posiciones = manager.dict()
    vehiculos_ids = manager.list()
    lock = Lock()

    limites = {
        "Norte->Sur": 250,
        "Sur->Norte": 350,
        "Oeste->Este": 250,
        "Este->Oeste": 350
    }
    destino_x = 600

    root = tk.Tk()
    print("[Rank 0 - GUI] Tkinter inicializado.")

    def agregar_vehiculo(via):
        print(f"[GUI] Solicitando agregar vehículo en: {via}")
        comm.send(via, dest=2, tag=10)  # Enviar orden a Rank 2

    gui = GUI(root, estados, posiciones, vehiculos_ids, lock, limites, destino_x, agregar_vehiculo)

    # Crear procesos de semáforos (estos sí pueden ser procesos)
    semaforos = {}
    for via in vias:
        s = Semaforo(nombre=via, estado_compartido=estados)
        s.start()
        semaforos[via] = s

    # Receptor MPI como hilo (no proceso)
    def recibir_mensajes_mpi():
        print("[Rank 0 - GUI] Escuchando mensajes MPI desde el controlador...")
        while True:
            grupo = comm.recv(source=1, tag=1)
            print(f"[GUI] Recibido grupo para cambiar a VERDE: {grupo}")

            for via in grupo:
                estados[via] = "verde"
            time.sleep(5)

            for via in grupo:
                estados[via] = "amarillo"
            time.sleep(2)

            for via in grupo:
                estados[via] = "rojo"

            comm.send("listo", dest=1, tag=2)
            print(f"[GUI] Grupo {grupo} completado")

    t_mpi = threading.Thread(target=recibir_mensajes_mpi, daemon=True)
    t_mpi.start()

    print("[Rank 0 - GUI] Ejecutando interfaz gráfica...")
    root.mainloop()

    # Al cerrar GUI
    for s in semaforos.values():
        s.join()
