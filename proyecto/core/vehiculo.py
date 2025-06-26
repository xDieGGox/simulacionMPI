from multiprocessing import Process
import time

class Vehiculo(Process):
    def __init__(self, id_, via, estado_semaforo, posiciones_compartidas, lock, limite_parada, destino, eliminar_despues=False, contador_cruces=None, tiempos_espera=None, lock_tiempo=None):
        super().__init__()
        self.id_vehiculo = id_
        self.via = via
        self.estado_semaforo = estado_semaforo
        self.posiciones = posiciones_compartidas
        self.lock = lock
        self.limite = limite_parada
        self.destino = destino
        self.direccion = self.detectar_direccion()
        self.eliminar_despues = eliminar_despues
        self.ha_cruzado = False
        self.tiempo_cruce = None
        self.contador_cruces = contador_cruces
        self.tiempos_espera = tiempos_espera
        self.tiempo_llegada = time.time() 
        self.lock_tiempo = lock_tiempo 

    def detectar_direccion(self):
        if "Norte->Sur" in self.via:
            return (0, 1)
        elif "Sur->Norte" in self.via:
            return (0, -1)
        elif "Oeste->Este" in self.via:
            return (1, 0)
        elif "Este->Oeste" in self.via:
            return (-1, 0)
        return (0, 0)
    
        
        
    def buscar_vehiculo_frente(self, pos):
        min_dist = float('inf')
        pos_frente = None
        for vid, p in self.posiciones.items():
            if vid == self.id_vehiculo:
                continue
            if self.mismo_carril(pos, p):
                d = self.distancia(pos, p)
                if 0 < d < min_dist:
                    min_dist = d
                    pos_frente = p
        return pos_frente

    def mismo_carril(self, p1, p2):
        if self.direccion[0] != 0:
            return abs(p1[1] - p2[1]) < 10 and (p2[0] - p1[0]) * self.direccion[0] > 0
        else:
            return abs(p1[0] - p2[0]) < 10 and (p2[1] - p1[1]) * self.direccion[1] > 0

    def distancia(self, p1, p2):
        return abs(p2[0] - p1[0]) - 10 + abs(p2[1] - p1[1])


    def run(self):
        while True:
            with self.lock:
                if self.id_vehiculo not in self.posiciones:
                    break

                pos = self.posiciones[self.id_vehiculo]
                avanzar = False

                # Obtener posición del vehículo de adelante
                frente = self.buscar_vehiculo_frente(pos)

                # Condición de avance
                if self.ha_cruzado:
                    avanzar = True
                elif self.estado_semaforo[self.via] == "verde":
                    avanzar = True
                else:
                    # distancia entre vehículos
                    if frente is None or self.distancia(pos, frente) >= 20:
                        if self.direccion[1] == 1 and pos[1] + 1 < self.limite:
                            avanzar = True
                        elif self.direccion[1] == -1 and pos[1] - 1 > self.limite:
                            avanzar = True
                        elif self.direccion[0] == 1 and pos[0] + 1 < self.limite:
                            avanzar = True
                        elif self.direccion[0] == -1 and pos[0] - 1 > self.limite:
                            avanzar = True

                if avanzar:
                    nueva_pos = [pos[0] + 1 * self.direccion[0], pos[1] + 1 * self.direccion[1]]
                    self.posiciones[self.id_vehiculo] = nueva_pos

                    if not self.ha_cruzado:
                        if self.direccion[1] == 1 and nueva_pos[1] >= self.limite:
                            self.ha_cruzado = True
                            self.tiempo_cruce = time.time()
                            if self.tiempos_espera is not None:
                                tiempo_espera = self.tiempo_cruce - self.tiempo_llegada
                                #print(f"[{self.via}] Tiempo de espera registrado: {tiempo_espera:.2f} segundos") 
                                if self.lock_tiempo:
                                    with self.lock_tiempo:
                                        self.tiempos_espera[self.via].append(tiempo_espera)
                                else:
                                    self.tiempos_espera[self.via].append(tiempo_espera)
                            if self.contador_cruces is not None:
                                self.contador_cruces[self.via] += 1
                        elif self.direccion[1] == -1 and nueva_pos[1] <= self.limite:
                            self.ha_cruzado = True
                            self.tiempo_cruce = time.time()
                            if self.tiempos_espera is not None:
                                tiempo_espera = self.tiempo_cruce - self.tiempo_llegada
                                #print(f"[{self.via}] Tiempo de espera registrado: {tiempo_espera:.2f} segundos")  # DEBUG
                                if self.lock_tiempo:
                                    with self.lock_tiempo:
                                        self.tiempos_espera[self.via].append(tiempo_espera)
                                else:
                                    self.tiempos_espera[self.via].append(tiempo_espera)
                            if self.contador_cruces is not None:
                                self.contador_cruces[self.via] += 1
                        elif self.direccion[0] == 1 and nueva_pos[0] >= self.limite:
                            self.ha_cruzado = True
                            self.tiempo_cruce = time.time()
                            if self.tiempos_espera is not None:
                                tiempo_espera = self.tiempo_cruce - self.tiempo_llegada
                                #print(f"[{self.via}] Tiempo de espera registrado: {tiempo_espera:.2f} segundos")  # DEBUG
                                if self.lock_tiempo:
                                    with self.lock_tiempo:
                                        self.tiempos_espera[self.via].append(tiempo_espera)
                                else:
                                    self.tiempos_espera[self.via].append(tiempo_espera)
                            if self.contador_cruces is not None:
                                self.contador_cruces[self.via] += 1
                        elif self.direccion[0] == -1 and nueva_pos[0] <= self.limite:
                            self.ha_cruzado = True
                            self.tiempo_cruce = time.time()
                            if self.tiempos_espera is not None:
                                tiempo_espera = self.tiempo_cruce - self.tiempo_llegada
                                #print(f"[{self.via}] Tiempo de espera registrado: {tiempo_espera:.2f} segundos")  # DEBUG
                                if self.lock_tiempo:
                                    with self.lock_tiempo:
                                        self.tiempos_espera[self.via].append(tiempo_espera)
                                else:
                                    self.tiempos_espera[self.via].append(tiempo_espera)
                            if self.contador_cruces is not None:
                                self.contador_cruces[self.via] += 1

                    if self.eliminar_despues and self.ha_cruzado:
                        if time.time() - self.tiempo_cruce >= 4:
                            del self.posiciones[self.id_vehiculo]
                            break

            time.sleep(0.009)  

