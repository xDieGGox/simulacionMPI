import time
import random
from multiprocessing import Process

class Semaforo(Process):
    def __init__(self, nombre, pipe, estado_compartido, vehiculos_en_espera, barrera, contador_cruces):
        super().__init__()
        self.nombre = nombre
        self.pipe = pipe
        self.estado_compartido = estado_compartido
        self.vehiculos_en_espera = vehiculos_en_espera
        self.barrera = barrera
        self.contador_cruces = contador_cruces

    def run(self):
        while True:
            permiso = self.pipe.recv()
            if permiso == "verde":
                
                cruzados_antes = self.contador_cruces[self.nombre]

                self.estado_compartido[self.nombre] = "verde"
                print(f"[{self.nombre}] SEMÁFORO EN VERDE")
                time.sleep(5)

                #Para filtrar vehículos que pertenecen a esta vía
                #vehiculos_via = [k for k in self.vehiculos_en_espera.keys() if self.nombre in k]
                #if vehiculos_via:
                    #avanzan = min(random.randint(1, 3), len(vehiculos_via))
                    #print(f"[{self.nombre}] Vehículos que cruzaron: {avanzan}")
                cruzados_despues = self.contador_cruces[self.nombre]
                total_cruzan = cruzados_despues - cruzados_antes
                print(f"[{self.nombre}] Vehículos que cruzaron: {total_cruzan}")

                self.estado_compartido[self.nombre] = "amarillo"
                print(f"[{self.nombre}] SEMÁFORO EN AMARILLO")
                time.sleep(2)

                self.estado_compartido[self.nombre] = "rojo"
                print(f"[{self.nombre}] SEMÁFORO EN ROJO")

                self.pipe.send("listo")

            self.barrera.wait()
