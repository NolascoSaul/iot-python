import multiprocessing as mp
import time


def print_word(pos, word, count, lock, result_list=None):
    printed = False

    while not printed:
        lock.acquire()
        try:
            if count.value == pos:
                print(word, flush=True, end=" ")
                if result_list is not None:
                    result_list.append(word)
                count.value += 1
                printed = True
        finally:
            lock.release()
     


def run_synchronization(result_list=None):
    words = ["Este", "es", "un", "ejemplo", "con", "siete", "procesos"]
    shared_count = mp.Value("i", 0)
    mutex = mp.Lock()

    processes = [
        mp.Process(
            target=print_word,
            args=(i, words[i], shared_count, mutex, result_list),
        )
        for i in range(7)
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    
    print()


def test_order(num_runs=20):
    expected_words = ["Este", "es", "un", "ejemplo", "con", "siete", "procesos"]

    for i in range(num_runs):
        with mp.Manager() as manager:
            result_list = manager.list()
            run_synchronization(result_list)
            obtained_words = list(result_list)

            if obtained_words != expected_words:
                print(f"Error en la iteración {i}:")
                print(f"Esperado: {expected_words}")
                print(f"Obtenido: {obtained_words}")
                return

    print(
        f"Prueba completada con éxito. Se ejecutaron {num_runs} pruebas correctamente."
    )


if __name__ == "__main__":
    test_order(20)
    print("\nSalida final:")
    run_synchronization()