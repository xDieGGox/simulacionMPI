from threading import Thread
import time
from core.utils import log
from mpi4py import MPI

class Vehiculo(Thread):
    def __init__(self, id, via, estados):
        super().__init__()
        self.id = id
        self.via = via
        self.estados = estados
        self.comm = MPI.COMM_WORLD

    def run(self):
        while True:
            estado = self.estados[self.via]
            if estado == "verde":
                self.comm.send(("vehiculo", self.via, "avanzando"), dest=2, tag=20)
                log(f"{self.id} avanzando", "VEHICULO")
            elif estado == "amarillo":
                self.comm.send(("vehiculo", self.via, "desacelerando"), dest=2, tag=20)
                log(f"{self.id} desacelerando", "VEHICULO")
            else:
                self.comm.send(("vehiculo", self.via, "detenido"), dest=2, tag=20)
                log(f"{self.id} detenido", "VEHICULO")
            time.sleep(1)
