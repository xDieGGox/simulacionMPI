# interfaz_mpi.py
from multiprocessing import Process, Manager, Lock
import tkinter as tk
import time
from gui.interfaz import GUI
from core.semaforo import Semaforo
from mpi4py import MPI

def iniciar_interfaz_semaforos(comm):
    rank = comm.Get_rank()
    assert rank == 0, "Este módulo debe ejecutarse solo en el rank 0"

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

    def agregar_vehiculo(via):
        print(f"[GUI] Solicitando agregar vehículo en: {via}")
        comm.send(via, dest=2, tag=10)  # Enviamos orden a nodo 2

    gui = GUI(root, estados, posiciones, vehiculos_ids, lock, limites, destino_x, agregar_vehiculo)

    semaforos = {}
    for via in vias:
        s = Semaforo(nombre=via, estado_compartido=estados)
        s.start()
        semaforos[via] = s

    def recibir_mensajes_mpi():
        while True:
            grupo = comm.recv(source=1, tag=1)
            print(f"[Rank 0 - GUI] Recibido grupo para cambiar a VERDE: {grupo}")

            for via in grupo:
                estados[via] = "verde"

            time.sleep(5)

            for via in grupo:
                estados[via] = "amarillo"
            time.sleep(2)

            for via in grupo:
                estados[via] = "rojo"

            comm.send("listo", dest=1, tag=2)
            print(f"[Rank 0 - GUI] Grupo {grupo} completado")

    p_mpi = Process(target=recibir_mensajes_mpi)
    p_mpi.start()

    print("[Rank 0 - GUI] Iniciando interfaz gráfica")
    root.mainloop()

    for s in semaforos.values():
        s.join()
    p_mpi.terminate()
