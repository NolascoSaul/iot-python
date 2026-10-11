import time
import numpy as np

N = 5000
matriz = np.ones((N, N), dtype=np.int32) ## ~100 MB, guardada fila tras fila (orden C)
def suma_por_filas(m):
    total = 0
    for i in range(m.shape[0]):
        total += int(m[i, :].sum()) # bloque contiguo: aprovecha la caché
    return total

def suma_por_columnas(m):
    total = 0
    for j in range(m.shape[1]):
        total += int(m[:, j].sum()) # saltos de N elementos: fallos de caché
    return total

for nombre, funcion in (("por filas", suma_por_filas), ("por columnas", suma_por_columnas)):
    inicio = time.perf_counter()
    resultado = funcion(matriz)
    print(f"Suma {nombre:<13}: {resultado} -> {time.perf_counter() - inicio:.3f} s")