import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mpi4py import MPI
import tkinter as tk
from core.utils import log

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank != 2:
    exit()

vias = ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]
colores = {"rojo": "red", "amarillo": "yellow", "verde": "green"}

estado_semaforos = {via: "rojo" for via in vias}
estado_vehiculos = {via: "detenido" for via in vias}

# Direcciones y posiciones iniciales visibles
direcciones = {
    "Norte->Sur": (0, 1),
    "Sur->Norte": (0, -1),
    "Oeste->Este": (1, 0),
    "Este->Oeste": (-1, 0)
}
offsets = {
    "Norte->Sur": [(300, -60), (300, -120), (300, -180)],
    "Sur->Norte": [(300, 660), (300, 720), (300, 780)],
    "Oeste->Este": [(-60, 300), (-120, 300), (-180, 300)],
    "Este->Oeste": [(660, 300), (720, 300), (780, 300)],
}

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tráfico Urbano")
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()

        self.vehiculos_gui = {}  # {"via": [veh1, veh2, veh3]}
        self.semaforos_gui = {}
        self.posiciones = {}

        self.dibujar_calles()
        self.crear_semaforos()
        self.crear_vehiculos()
        self.actualizar()

    def dibujar_calles(self):
        self.canvas.create_rectangle(250, 0, 350, 600, fill="lightgray", outline="")
        self.canvas.create_rectangle(0, 250, 600, 350, fill="lightgray", outline="")
        for y in range(0, 600, 20):
            self.canvas.create_line(300, y, 300, y + 10, fill="white", width=2)
        for x in range(0, 600, 20):
            self.canvas.create_line(x, 300, x + 10, 300, fill="white", width=2)

    def crear_semaforos(self):
        self.semaforos_gui["Norte->Sur"] = self.canvas.create_oval(275, 260, 285, 270, fill="red")
        self.semaforos_gui["Sur->Norte"] = self.canvas.create_oval(315, 330, 325, 340, fill="red")
        self.semaforos_gui["Oeste->Este"] = self.canvas.create_oval(260, 275, 270, 285, fill="red")
        self.semaforos_gui["Este->Oeste"] = self.canvas.create_oval(330, 315, 340, 325, fill="red")

    def crear_vehiculos(self):
        for via in vias:
            self.vehiculos_gui[via] = []
            for i, (x, y) in enumerate(offsets[via]):
                veh = self.canvas.create_rectangle(x, y, x + 10, y + 20, fill="blue")
                self.vehiculos_gui[via].append(veh)
                self.posiciones[(via, i)] = [x, y]

    def mover_vehiculos(self):
        for via in vias:
            dx, dy = direcciones[via]
            velocidad = 0
            if estado_vehiculos[via] == "avanzando":
                velocidad = 4
            elif estado_vehiculos[via] == "desacelerando":
                velocidad = 2

            for i in range(3):
                pos = self.posiciones[(via, i)]
                pos[0] += dx * velocidad
                pos[1] += dy * velocidad

                # Reposicionar si sale del canvas
                if via == "Norte->Sur" and pos[1] > 620:
                    pos[1] = -40
                elif via == "Sur->Norte" and pos[1] < -40:
                    pos[1] = 640
                elif via == "Oeste->Este" and pos[0] > 620:
                    pos[0] = -40
                elif via == "Este->Oeste" and pos[0] < -40:
                    pos[0] = 640

                self.canvas.coords(
                    self.vehiculos_gui[via][i],
                    pos[0], pos[1], pos[0] + 10, pos[1] + 20
                )

    def actualizar(self):
        while comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG):
            tipo, via, estado = comm.recv(source=MPI.ANY_SOURCE)
            print(f"[RECEIVED] tipo={tipo}, via={via}, estado={estado}")  # DEBUG
            if tipo == "vehiculo":
                estado_vehiculos[via] = estado
            elif tipo == "semaforo":
                estado_semaforos[via] = estado

        for via in vias:
            self.canvas.itemconfig(self.semaforos_gui[via], fill=colores[estado_semaforos[via]])

        self.mover_vehiculos()
        self.root.after(100, self.actualizar)

# Inicia GUI
root = tk.Tk()
gui = GUI(root)
root.mainloop()
