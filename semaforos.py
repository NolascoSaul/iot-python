import threading
import time

lugares_ocupados = 0
total_lugares = 6
mutex = threading.Lock()

semaforo_compactos = threading.Semaphore(3)
semaforo_grandes = threading.Semaphore(3)


def auto(id_auto, tipo, semaforo):
    global lugares_ocupados

    print(f"Auto {id_auto} ({tipo}): LLEGA. Esperando lugar...")

    semaforo.acquire()

    mutex.acquire()
    lugares_ocupados += 1
    print(
        f"Auto {id_auto} ({tipo}): ESTACIONADO. Ocupados: {lugares_ocupados}/{total_lugares}"
    )
    mutex.release()

    time.sleep(2)  # Simula el tiempo estacionado

    mutex.acquire()
    lugares_ocupados -= 1
    print(
        f"Auto {id_auto} ({tipo}): SALE. Ocupados: {lugares_ocupados}/{total_lugares}"
    )
    mutex.release()

    semaforo.release()
    
if __name__ == "__main__":
    configuracion_autos = [
        (1, "Compacto", semaforo_compactos),
        (2, "Grande", semaforo_grandes),
        (3, "Compacto", semaforo_compactos),
        (4, "Grande", semaforo_grandes),
        (5, "Compacto", semaforo_compactos),
        (6, "Grande", semaforo_grandes),
        (7, "Compacto", semaforo_compactos),
        (8, "Grande", semaforo_grandes),
    ]

    hilos = []

    for id_a, t_auto, sem in configuracion_autos:
        hilo = threading.Thread(target=auto, args=(id_a, t_auto, sem))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    print(
        f"\n--- TODOS LOS AUTOS HAN SALIDO ---\nVerificación final: Lugares ocupados totales: {lugares_ocupados}"
    )