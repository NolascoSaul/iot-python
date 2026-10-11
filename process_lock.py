import multiprocessing as mp

def incrementar(contador, lock):
    """Función que incrementa un contador compartido de forma segura."""
    # El 'lock.acquire()' garantiza la Exclusión Mutua.
    lock.acquire() # 1. Intenta adquirir la cerradura (ENTRA a la Sección Crítica)
    try:
        # Esto es la Sección Crítica: Solo un proceso puede estar aquí a la vez.
        contador.value += 1
    finally:
        lock.release() # 2. Libera la cerradura (SALE de la Sección Crítica)

if __name__ == "__main__":
    # Variable compartida (Shared Value) y el objeto Lock
    contador_compartido = mp.Value('i', 0)
    mutex = mp.Lock()
    # Creación de 10 procesos que intentan modificar la misma variable
    procesos = [mp.Process(target=incrementar, args=(contador_compartido,
    mutex)) for _ in range(10)]
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()
    # Gracias al Lock, el resultado es predecible y correcto.
    print(f"\nValor final del contador (Sincronizado): {contador_compartido.value}")
    # El resultado SIEMPRE es 10. Sin el lock, sería inconsistente.