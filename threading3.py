import threading
import time

# Recurso de Sincronización
balance_condition = threading.Condition()
stop_event = threading.Event() # NUEVO: Variable de control para señal de parada
balance = 0
MONTO_RETIRO = 5 

def depositar(cantidad):
    global balance
    with balance_condition: 
        print(f"[DEPOSITAR] Depositando {cantidad}...")
        balance += cantidad
        print(f"[DEPOSITAR] Saldo actual: {balance}. Notificando a todos...")
        balance_condition.notify_all() 

def retirar(id_hilo):
    global balance
    
    with balance_condition:
        # Condición de bucle MÁS SEGURA: Espera mientras el balance es insuficiente Y NO ha recibido la señal de parada
        while balance < MONTO_RETIRO and not stop_event.is_set():
            print(f"[HILO {id_hilo}] Saldo bajo ({balance}). Esperando depósito o señal de parada...")
            
            # .wait() regresa al bucle cuando es notificado,
            # lo que nos permite verificar la condición Y el stop_event.
            balance_condition.wait() 
            
        # NUEVA CONDICIÓN DE SALIDA: Si la señal de parada está activa, el hilo debe terminar.
        if stop_event.is_set() and balance < MONTO_RETIRO:
            print(f"[HILO {id_hilo}] Operación cancelada. El banco cerró.")
            return

        # Si sale del while Y NO es por el stop_event, es porque retiró con éxito.
        if balance >= MONTO_RETIRO:
            print(f"[HILO {id_hilo}] Condición cumplida. Retirando {MONTO_RETIRO}...")
            balance -= MONTO_RETIRO
            print(f"[HILO {id_hilo}] Retiro OK. Saldo final: {balance}")


if __name__ == "__main__":
    
    hilos_retiro = [threading.Thread(target=retirar, args=(i,)) for i in range(3)]
    
    hilo_deposito_1 = threading.Thread(target=depositar, args=(3,)) 
    hilo_deposito_2 = threading.Thread(target=depositar, args=(7,)) 
    
    # Iniciar hilos de retiro
    for t in hilos_retiro:
        t.start()
        
    time.sleep(1) # Dejar que los hilos se bloqueen

    # Iniciar depósitos
    hilo_deposito_1.start()
    hilo_deposito_1.join()

    time.sleep(1) 

    hilo_deposito_2.start()
    hilo_deposito_2.join()
    
    # --- LA PARTE CRÍTICA ---
    # 1. Activamos la señal de parada
    stop_event.set() 
    # 2. Notificamos a todos los hilos dormidos para que comprueben la señal de parada
    with balance_condition:
        balance_condition.notify_all() 
    # 3. Esperamos que todos terminen
    for t in hilos_retiro:
        t.join()

    print("\n--- EJECUCIÓN FINALIZADA Y SIN INTERBLOQUEO ---")
    print(f"Saldo final esperado: 0")
    print(f"Saldo final real: {balance}")