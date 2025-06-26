# main_mpi.py
from mpi4py import MPI
from proyecto.core.vehiculos_mpi import iniciar_generador_vehiculos
from proyecto.gui.interfaz_mpi import iniciar_interfaz_semaforos
import time

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        # Nodo 0: GUI y semáforos
        iniciar_interfaz_semaforos(comm)

        # Mantener vivo el proceso 0 (importante en Windows)
        while True:
            time.sleep(1)

    elif rank == 1:
        # Nodo 1: Controlador de tráfico
        from proyecto.core.controlador_mpi import iniciar_controlador_mpi
        iniciar_controlador_mpi(comm)

    elif rank == 2:
        # Nodo 2: Generador de vehículos
        iniciar_generador_vehiculos(comm)

    else:
        print(f"[Rank {rank}] No asignado a ninguna función específica.")

if __name__ == "__main__":
    main()
