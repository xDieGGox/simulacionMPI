from mpi4py import MPI
import tkinter as tk
from core.utils import log

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank != 2:
    exit()

vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]
estados_vehiculos = {via: "detenido" for via in vias}
estados_semaforos = {via: "rojo" for via in vias}

class SimulacionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tráfico MPI")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()
        self.info = tk.Label(root, text="Estado", font=("Arial", 10))
        self.info.pack()
        self.root.after(100, self.actualizar)

    def actualizar(self):
        while comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG):
            msg = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
            tipo, via, estado = msg
            if tipo == "vehiculo":
                estados_vehiculos[via] = estado
            else:
                estados_semaforos[via] = estado

        texto = "\n".join([
            f"{via}: Semáforo={estados_semaforos[via]}, Vehículo={estados_vehiculos[via]}"
            for via in vias
        ])
        self.info.config(text=texto)
        self.root.after(500, self.actualizar)

root = tk.Tk()
app = SimulacionGUI(root)
root.mainloop()
