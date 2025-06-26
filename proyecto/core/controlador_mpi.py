# core/controlador_mpi.py
from mpi4py import MPI
import time

def iniciar_controlador_mpi(comm):
    rank = comm.Get_rank()
    assert rank == 1, "Este archivo debe ejecutarse solo en rank 1"

    vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]
    grupos = [
        ["Norte->Sur", "Sur->Norte"],
        ["Este->Oeste", "Oeste->Este"]
    ]

    total_cruzados = {via: 0 for via in vias}
    espera_promedio = {via: 0 for via in vias}
    ciclos = 3

    print(f"[Rank 1 - Controlador] Iniciando simulación por {ciclos} ciclos")

    for ciclo in range(ciclos):
        print(f"\n[Ciclo {ciclo+1}] Iniciando grupo de semáforos...")

        for grupo in grupos:
            comm.send(grupo, dest=0, tag=1)
            confirmacion = comm.recv(source=0, tag=2)
            print(f"[Controlador] Confirmación de grupo {grupo}: {confirmacion}")

        # Recibe estadísticas de vehículos cruzados desde rank 2 (vehículos)
        cruzados = comm.recv(source=2, tag=3)
        print(f"[Controlador] Datos recibidos desde generador: {cruzados}")

        for via in cruzados:
            total_cruzados[via] += cruzados[via]

        time.sleep(1)

    # Reducir totales para una vía como ejemplo usando reduce
    reduccion_norte_sur = comm.reduce(total_cruzados["Norte->Sur"], op=MPI.SUM, root=1)

    print("\n===== REPORTE FINAL =====")
    for via in vias:
        print(f"Vía: {via}")
        print(f"  - Total vehículos cruzados: {total_cruzados[via]}")
    print(f"  - Reducción total (Norte->Sur): {reduccion_norte_sur}")
