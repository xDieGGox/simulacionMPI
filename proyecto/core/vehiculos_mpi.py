# core/vehiculos_mpi.py
from mpi4py import MPI
from multiprocessing import Process, Manager, Lock
import time
from proyecto.core.vehiculo import Vehiculo
from proyecto.core.semaforo import Semaforo

def iniciar_generador_vehiculos(comm):
    rank = comm.Get_rank()
    assert rank == 2, "Este archivo debe ejecutarse solo en el rank 2"

    vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]

    manager = Manager()
    estados = manager.dict({via: "rojo" for via in vias})  # Luz inicial
    posiciones = manager.dict()
    vehiculos_cruzados = manager.dict({via: 0 for via in vias})
    tiempos_espera = manager.dict({via: manager.list() for via in vias})
    lock = Lock()
    lock_tiempo = manager.Lock()

    posiciones_iniciales = {
        "Norte->Sur": (275, 0),
        "Sur->Norte": (315, 600),
        "Oeste->Este": (0, 275),
        "Este->Oeste": (600, 315),
    }

    limites = {
        "Norte->Sur": 250,
        "Sur->Norte": 350,
        "Oeste->Este": 250,
        "Este->Oeste": 350,
    }

    destino_y = 600
    destino_x = 600

    vehiculos = []

    def crear_vehiculo(via, i):
        vid = f"{via}-{i}"
        x, y = posiciones_iniciales[via]
        posiciones[vid] = [x, y]
        destino = destino_y if "Norte" in via or "Sur" in via else destino_x

        v = Vehiculo(
            id_=vid,
            via=via,
            estado_semaforo=estados,
            posiciones_compartidas=posiciones,
            lock=lock,
            limite_parada=limites[via],
            destino=destino,
            eliminar_despues=True,
            contador_cruces=vehiculos_cruzados,
            tiempos_espera=tiempos_espera,
            lock_tiempo=lock_tiempo
        )
        v.start()
        vehiculos.append(v)

    # Vehículos iniciales
    for via in vias:
        for i in range(2):
            crear_vehiculo(via, i)

    # Escucha de nuevos vehículos desde GUI
    def escuchar_nuevos_vehiculos():
        while True:
            if comm.Iprobe(source=0, tag=10):
                via = comm.recv(source=0, tag=10)
                count = len([k for k in posiciones.keys() if via in k])
                print(f"[Vehículos] Agregando vehículo nuevo en {via}")
                crear_vehiculo(via, count)
            time.sleep(0.1)

    listener = Process(target=escuchar_nuevos_vehiculos)
    listener.start()

    # Esperar 20 segundos antes de enviar resumen (luego puedes adaptar a recibir señal)
    time.sleep(20)

    resumen_cruces = {via: vehiculos_cruzados[via] for via in vias}
    comm.send(resumen_cruces, dest=1, tag=3)
    print(f"[Rank 2 - Vehículos] Enviado resumen: {resumen_cruces}")

    for v in vehiculos:
        v.join()
    listener.terminate()
    print("[Rank 2 - Vehículos] Finalizado")
