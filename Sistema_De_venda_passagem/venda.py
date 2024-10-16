import threading
import queue
import random
import time
import json
from faker import Faker

fake = Faker('pt_BR')

fila = queue.Queue()

# seção crítica
lock = threading.Lock()

def produtor():
    while True:
        with lock:
            for _ in range(20):
                dados_passagem = {
                    "nome": fake.name(),
                    "cpf": fake.cpf(),
                    "data": fake.date_this_year().strftime("%d/%m/%Y"),
                    "hora": fake.time(),
                    "assento": random.randint(1, 100)
                }
                print("Demanda gerada:")
                for chave, valor in dados_passagem.items():
                    print(f"{chave}: {valor}")
                print("-" * 20)

                json_dados = json.dumps(dados_passagem)
                fila.put(json_dados)
        time.sleep(3)

def consumidor():
    while True:
        with lock:
            for _ in range(10):
                if not fila.empty():
                    dados = fila.get()
                    fila.task_done()
                    print(f"Demanda consumida: {dados}")
        time.sleep(3)

if __name__ == "__main__":
    # Cria e inicia
    thread_produtor = threading.Thread(target=produtor)
    thread_consumidor = threading.Thread(target=consumidor)

    thread_produtor.start()
    thread_consumidor.start()

    # Aguarda as threads terminarem (infinito)
    thread_produtor.join()
    thread_consumidor.join()