from multiprocessing import Process
import time
import random

class Vehiculo(Process):
    def __init__(self, id_, via, estados_compartidos):
        super().__init__()
        self.id = id_
        self.via = via
        self.estados = estados_compartidos

    def run(self):
        while True:
            estado = self.estados[self.via]
            if estado == "verde":
                print(f"Vehículo {self.id} avanzando por {self.via}")
            elif estado == "amarillo":
                print(f"Vehículo {self.id} desacelerando por {self.via}")
            else:
                print(f"Vehículo {self.id} detenido en {self.via}")
            time.sleep(random.uniform(0.5, 1.0))
