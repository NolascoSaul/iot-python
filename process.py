import multiprocessing
import time
import os
def tarea_sensor(nombre):
    """Simula una tarea de lectura de sensor en robótica."""
    # Obtiene el ID del proceso hijo
    print(f"[{nombre}] PID: {os.getpid()} - Iniciando lectura...")
    time.sleep(1.5) # Simula tiempo de procesamiento de datos
    print(f"[{nombre}] Lectura de datos completa.")
    
if __name__ == "__main__":
    # El proceso principal crea dos procesos hijos (Concurrencia)
    proceso_camara = multiprocessing.Process(target=tarea_sensor,
    args=("Camara_RGB",))
    proceso_gps = multiprocessing.Process(target=tarea_sensor,
    args=("GPS_Localizador",))
    proceso_camara.start() # Pone el proceso en estado Listo
    proceso_gps.start() # Pone el proceso en estado Listo
    # El proceso principal espera a que los hijos terminen su ejecución
    proceso_camara.join()
    proceso_gps.join()
    print("\n[Principal] Todas las tareas de sensado han finalizado.")
    # El SO administró y planificó la ejecución concurrente de ambos procesos.