import tkinter as tk

class GUI:
    def __init__(self, root, estados, posiciones, vehiculos_ids, lock, limites, destino_x, callback_agregar):
        self.root = root
        self.estados = estados
        self.posiciones = posiciones
        self.vehiculos_ids = vehiculos_ids
        self.lock = lock
        self.limites = limites
        self.destino_x = destino_x
        self.callback_agregar = callback_agregar

        self.root.title("Tráfico Urbano")
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()

        self.semaforos_gui = {}
        self.rectangulos_vehiculo = {}

        self.dibujar_calles()
        self.crear_semaforos()
        self.crear_botones_agregar()
        self.crear_rectangulos_vehiculo()
        self.actualizar_gui()

    def dibujar_calles(self):
        self.canvas.create_rectangle(250, 0, 350, 600, fill="lightgray", outline="")  # Calle vertical
        
        

        #self.canvas.create_rectangle(279, 0, 281, 600, fill="gray")  # Norte->Sur
        #self.canvas.create_rectangle(319, 0, 321, 600, fill="gray")  # Sur->Norte

        self.canvas.create_rectangle(0, 250, 600, 350, fill="lightgray", outline="")  # Calle horizontal
        # Línea punteada blanca vertical
        for y in range(0, 600, 20):  # de 0 a 600 en pasos de 20 píxeles
            self.canvas.create_line(300, y, 300, y + 10, fill="white", width=2)

        # Línea punteada blanca horizontal
        for x in range(0, 600, 20):
            self.canvas.create_line(x, 300, x + 10, 300, fill="white", width=2)

        ##NOMBRES DE LAS CALLES
        self.canvas.create_text(310, 100, text="Av. Turuhuayco", fill="black", angle=90, font=("Arial", 10, "bold"))
        self.canvas.create_text(400, 290, text="Calle Vieja", fill="black", font=("Arial", 10, "bold"))

        #self.canvas.create_rectangle(0, 270, 600, 290, fill="gray")  # Oeste->Este
        #self.canvas.create_rectangle(0, 310, 600, 330, fill="gray")  # Este->Oeste

        ##CUADROS DE LAS CALLES O VIVIENDAS
        #CUADRANTE SUPERIOR IZQUIERDO
        #UPS
        self.canvas.create_rectangle(60, 60, 180, 180, fill="lightblue", outline="black", width=2)
        self.canvas.create_text(120, 50, text="UPS", font=("Arial", 12, "bold"))

        # Ventanas del edificio UPS
        for i in range(3):  # filas
            for j in range(3):  # columnas
                x0 = 75 + j*30
                y0 = 80 + i*30
                self.canvas.create_rectangle(x0, y0, x0+15, y0+15, fill="white", outline="gray")
        
        #Estudiantes
        personas_coords = [(90, 190), (120, 195), (150, 185)]

        for x, y in personas_coords:
            #cabeza
            self.canvas.create_oval(x, y, x+6, y+6, fill="peachpuff", outline="black")
            #cuerpo
            self.canvas.create_line(x+3, y+6, x+3, y+16, fill="black")
            #brazos
            self.canvas.create_line(x-2, y+10, x+8, y+10, fill="black")
            #piernas
            self.canvas.create_line(x+3, y+16, x-1, y+22, fill="black")
            self.canvas.create_line(x+3, y+16, x+7, y+22, fill="black")


        #CUADRANTE SUPERIOR DERECHO
        #ZAPATERIA
        self.canvas.create_rectangle(420, 60, 520, 160, fill="#d9b38c", outline="black", width=2)
        self.canvas.create_text(470, 50, text="Zapatería", font=("Arial", 10, "bold"))

        #casasitas
        casas_sd_coords = [(380, 180), (550, 180), (400, 100), (540, 100)]
        for x, y in casas_sd_coords:
            self.canvas.create_rectangle(x, y, x+30, y+30, fill="beige", outline="black")
            self.canvas.create_text(x+15, y+15, text="Casa", font=("Arial", 7))

        #CUADRANTE INFERIOR IZQUIERDO:
        for i in range(2):
            for j in range(3):
                x0 = 60 + j*50
                y0 = 380 + i*60
                self.canvas.create_rectangle(x0, y0, x0+40, y0+40, fill="beige", outline="black")
                if j == 0:  #las más cercanas a la calle horizontal
                    self.canvas.create_text(x0+20, y0+20, text="Rest.", font=("Arial", 7))
                else:
                    self.canvas.create_text(x0+20, y0+20, text="Casa", font=("Arial", 7))

        #CUADRANTE INFERIOR DERECHO
        casas_id_coords = [(400, 380), (470, 380), (540, 380),
                        (400, 450), (470, 450), (540, 450),
                        (400, 520), (470, 520), (540, 520)]
        for x, y in casas_id_coords:
            self.canvas.create_rectangle(x, y, x+40, y+40, fill="beige", outline="black")
            self.canvas.create_text(x+20, y+20, text="Casa", font=("Arial", 7))

    def crear_semaforos(self):
        self.semaforos_gui["Norte->Sur"] = self.canvas.create_oval(275, 260, 285, 270, fill="red")
        self.semaforos_gui["Sur->Norte"] = self.canvas.create_oval(315, 330, 325, 340, fill="red")
        self.semaforos_gui["Oeste->Este"] = self.canvas.create_oval(260, 275, 270, 285, fill="red")
        self.semaforos_gui["Este->Oeste"] = self.canvas.create_oval(330, 315, 340, 325, fill="red")

    def crear_botones_agregar(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        for via in ["Norte->Sur", "Sur->Norte", "Este->Oeste", "Oeste->Este"]:
            btn = tk.Button(frame, text=f"Agregar {via}", command=lambda v=via: self.callback_agregar(v))
            btn.pack(side="left", padx=5)

    def crear_rectangulos_vehiculo(self):
        for vid in self.vehiculos_ids:
            x, y = self.posiciones[vid]
            self.rectangulos_vehiculo[vid] = self.canvas.create_rectangle(x, y, x+10, y+20, fill="blue")

    def registrar_vehiculo_gui(self, vid):
        """Permite a la GUI registrar un nuevo vehículo (usado desde main al agregar vehículos dinámicamente)."""
        x, y = self.posiciones[vid]
        self.rectangulos_vehiculo[vid] = self.canvas.create_rectangle(x, y, x+10, y+20, fill="blue")

    def actualizar_gui(self):
        colores = {"rojo": "red", "amarillo": "yellow", "verde": "green"}
        for via in self.semaforos_gui:
            estado = self.estados[via]
            self.canvas.itemconfig(self.semaforos_gui[via], fill=colores[estado])

        #Actualizacion de vehiculos que existen
        vehiculos_a_eliminar = []
        for vid, rect_id in self.rectangulos_vehiculo.items():
            if vid in self.posiciones:
                x, y = self.posiciones[vid]
                self.canvas.coords(rect_id, x, y, x+10, y+20)
            else:
                vehiculos_a_eliminar.append(vid)

        #eliminar rectángulos de vehículos que ya no existen
        for vid in vehiculos_a_eliminar:
            self.canvas.delete(self.rectangulos_vehiculo[vid])
            del self.rectangulos_vehiculo[vid]

        self.root.after(100, self.actualizar_gui)
