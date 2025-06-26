# main_mpi.py
from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        # Nodo 0: GUI y semáforos
        from gui.interfaz_mpi import iniciar_interfaz_semaforos
        iniciar_interfaz_semaforos(comm)

    elif rank == 1:
        # Nodo 1: Controlador de tráfico
        from core.controlador_mpi import iniciar_controlador_mpi
        iniciar_controlador_mpi(comm)

    elif rank == 2:
        # Nodo 2: Generador de vehículos
        from core.vehiculos_mpi import iniciar_generador_vehiculos
        iniciar_generador_vehiculos(comm)

    else:
        print(f"[Rank {rank}] No asignado a ninguna función específica.")

if __name__ == "__main__":
    main()
