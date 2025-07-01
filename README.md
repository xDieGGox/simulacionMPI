# Simulación de Tráfico Vehicular Distribuido con MPI

Este proyecto simula el flujo de vehículos en una intersección urbana utilizando **MPI** para la comunicación entre nodos distribuidos, **Tkinter** para la visualización y **multithreading** para la gestión concurrente de entidades.

## Estructura del Proyecto

```
mpi/
├── main_selector.py             # Archivo principal de entrada MPI
├── nodo_controlador/
│   └── controlador_mpi.py       # Lógica del controlador de semáforos
├── nodo_vehiculos/
│   └── vehiculos_mpi.py         # Lógica de los vehículos
├── nodo_gui/
│   └── interfaz_mpi.py          # GUI gráfica con Tkinter
├── core/
│   ├── vehiculo.py              # Clase Vehiculo (thread)
│   ├── utils.py                 # Funciones comunes (log, etc.)
│   └── tklog.py                 # Ventana de logs locales
```

## Requisitos

- Python 3.9
- `mpi4py`
- `Tkinter` (instalado por defecto en la mayoría de entornos Python)
- Microsoft MPI (en Windows): https://learn.microsoft.com/en-us/message-passing-interface/microsoft-mpi

Instalación de dependencias:
```bash
pip install mpi4py
```

## Ejecución local

```bash
mpiexec -n 3 python main_selector.py
```

Esto inicia los tres procesos:

- Rank 0: Nodo de vehículos
- Rank 1: Nodo de controlador
- Rank 2: Nodo de GUI

## Ejecución distribuida (en red LAN) para el Clúster

Ejemplo con 3 máquinas:

```bash
mpiexec -hosts 3 192.168.1.10 1 192.168.1.11 1 192.168.1.12 1 -l python main_selector.py
```

Asegúrate de:

- Tener el **smpd** corriendo en todas las máquinas (`smpd -d`)
- Tener las claves SSH/configuraciones equivalentes si usas Linux
- Que el código esté **sincronizado** (idéntico) en todas las máquinas

## ¿Qué hace cada nodo?

- `vehiculos_mpi.py`: Lanza vehículos como hilos, que avanzan según el estado del semáforo recibido por MPI.
- `controlador_mpi.py`: Controla la lógica de los semáforos, emite cambios de estado usando `send()` y `Bcast()`.
- `interfaz_mpi.py`: Dibuja los semáforos y vehículos en pantalla con movimiento y actualización visual en tiempo real.

## Técnicas utilizadas

- Comunicación **punto a punto** (`send`, `recv`)
- Comunicación **colectiva** (`MPI.Bcast`)
- Sincronización básica con **hilos** (`threading`)
- GUI con **Tkinter**
- Arquitectura distribuida con **3 procesos diferentes** en diferentes máquinas
