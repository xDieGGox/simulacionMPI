@echo off
title Simulador de Tráfico MPI - Windows Local

start "GUI (Rank 0)" cmd /k python -m proyecto.gui.interfaz_mpi
start "Controlador (Rank 1)" cmd /k python -m proyecto.core.controlador_mpi
start "Vehículos (Rank 2)" cmd /k python -m proyecto.core.vehiculos_mpi
