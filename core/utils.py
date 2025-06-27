from datetime import datetime

def log(mensaje, origen=""):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {origen}: {mensaje}")
