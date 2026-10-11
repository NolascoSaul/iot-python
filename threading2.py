import threading
import time

# 1. Objeto de Sincronización: Condition
# Una Variable de Condición incluye un Lock (Mutex) implícito que debe usarse
# para acceder a los recursos compartidos.
balance_condition = threading.Condition()
balance = 0
MONTO_RETIRO = 5  # La cantidad que intentará retirar cada hilo.

def depositar(cantidad):
    """Función para depositar y notificar a los hilos en espera."""
    global balance
    
    # 2. Adquirir el Lock (parte de la Condition)
    with balance_condition: 
        print(f"[DEPOSITAR] Depositando {cantidad}...")
        balance += cantidad
        print(f"[DEPOSITAR] Saldo actual: {balance}. Notificando a todos...")
        
        # 3. Notificar: Despierta a todos los hilos que están esperando (wait)
        balance_condition.notify_all() 

def retirar(id_hilo):
    """Función para retirar fondos, esperando si el saldo es insuficiente."""
    global balance
    
    # 4. Adquirir el Lock
    with balance_condition:
        # Loop de espera: El hilo espera hasta que la condición (balance >= MONTO_RETIRO) sea verdadera
        while balance < MONTO_RETIRO:
            print(f"[HILO {id_hilo}] Saldo bajo ({balance}). Esperando depósito...")
            
            # 5. Esperar: Libera el Lock y se suspende, esperando una notificación.
            # Cuando despierta, readquiere el Lock.
            balance_condition.wait() 

        # Si sale del while, es porque la condición se cumplió.
        print(f"[HILO {id_hilo}] Condición cumplida. Retirando {MONTO_RETIRO}...")
        balance -= MONTO_RETIRO
        print(f"[HILO {id_hilo}] Retiro OK. Saldo final: {balance}")

if __name__ == "__main__":
    
    # Hilos Consumidores (intentarán retirar inmediatamente, se bloquearán)
    hilos_retiro = [threading.Thread(target=retirar, args=(i,)) for i in range(3)]
    
    # Hilos Productores (harán un depósito secuencial después de un breve retraso)
    hilo_deposito_1 = threading.Thread(target=depositar, args=(3,)) # Depósito insuficiente
    hilo_deposito_2 = threading.Thread(target=depositar, args=(7,)) # Depósito suficiente para algunos
    
    # 1. Iniciar hilos de retiro (se bloquearán en .wait())
    for t in hilos_retiro:
        t.start()
        
    time.sleep(1) # Esperar a que los hilos de retiro se bloqueen

    # 2. Iniciar depósitos
    hilo_deposito_1.start()
    hilo_deposito_1.join() # Esperar el primer depósito

    time.sleep(1) 

    hilo_deposito_2.start()
    hilo_deposito_2.join() # Esperar el segundo depósito
    
    for t in hilos_retiro:
        t.join()

    print("\n--- EJECUCIÓN FINALIZADA ---")
    print(f"Saldo final esperado: {3 + 7 - 5*2} (asumiendo que 2 hilos retiraron)")
    print(f"Saldo final real: {balance}")