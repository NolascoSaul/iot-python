import threading
import time
import os

def procesar_noticia(nombre_archivo, nombre_hilo, lock):
    print(f"[{nombre_hilo}] Leyendo: {nombre_archivo}...")
    time.sleep(1)

    with open(nombre_archivo, "r") as f:
        contenido = f.read()

    lock.acquire()
    try:
        with open("reporte_final.txt", "a") as f_salida:
            f_salida.write(contenido + "\n")
        print(f"[{nombre_hilo}] Escritura en Reporte OK.")
    finally:
        lock.release()
        
def preparar_archivos():
    noticias = [
        "El Lunes no habrá clases de IoT",
        "El miércoles pasado la clase fue en línea",
        "El Jueves habrá examen",
        "El viernes es el último día del segundo periodo",
        "El próximo lunes empieza la semana Tec",
    ]

    for i, texto in enumerate(noticias, 1):
        with open(f"noticia_{i}.txt", "w") as f:
            f.write(texto)

    with open("reporte_final.txt", "w") as f:
        pass
    
def limpiar_archivos():
    for i in range(1, 6):
        nombre = f"noticia_{i}.txt"
        if os.path.exists(nombre):
            os.remove(nombre)


if __name__ == "__main__":
    preparar_archivos()

    print("--- INICIO DE AGREGACIÓN CONCURRENTE ---")

    lock = threading.Lock()
    hilos = []

    for i in range(1, 6):
        nombre_archivo = f"noticia_{i}.txt"
        nombre_hilo = f"Hilo_Lectura_{i}"
        hilo = threading.Thread(
            target=procesar_noticia,
            args=(nombre_archivo, nombre_hilo, lock),
        )
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print("\n--- PROCESO DE AGREGACIÓN FINALIZADO ---")
    print(
        "Revise el archivo 'reporte_final.txt' para ver el resultado sincronizado."
    )

    limpiar_archivos()
    print("Archivos fuente temporales eliminados.")