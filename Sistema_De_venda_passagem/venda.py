import threading
import queue
import random
import time
import json
from faker import Faker

# Inicializa o gerador de dados fake
fake = Faker('pt_BR')

# Inicializa a fila
fila = queue.Queue()

# Lock para proteger a seção crítica
lock = threading.Lock()

# Função para gerar dados de passagem (produtor)
def gerar_demanda():
    while True:
        with lock:
            for _ in range(20):  # Gerar 20 demandas a cada 3 segundos
                dados_passagem = {
                    "nome": fake.name(),
                    "cpf": fake.cpf(),
                    "data": fake.date_this_year().strftime("%d/%m/%Y"),
                    "hora": fake.time(),
                    "assento": random.randint(1, 100)
                }
                # Imprimir dados verticalmente
                print("Demanda gerada:")
                for chave, valor in dados_passagem.items():
                    print(f"{chave}: {valor}")
                print("-" * 20)  # Separador para cada demanda

                json_dados = json.dumps(dados_passagem)
                fila.put(json_dados)
        time.sleep(3)  # Espera 3 segundos para gerar mais demandas

# Função para processar as demandas da fila (consumidor)
def consumir_demanda():
    while True:
        with lock:
            for _ in range(10):  # Consumir 10 demandas a cada 3 segundos
                if not fila.empty():
                    dados = fila.get()
                    fila.task_done()
                    print(f"Demanda consumida: {dados}")
        time.sleep(3)  # Espera 3 segundos para consumir mais demandas

# Programa principal
if __name__ == "__main__":
    # Cria e inicia as threads dos produtores e consumidores
    thread_produtor = threading.Thread(target=gerar_demanda)
    thread_consumidor = threading.Thread(target=consumir_demanda)

    thread_produtor.start()
    thread_consumidor.start()

    # Aguarda as threads terminarem (infinito)
    thread_produtor.join()
    thread_consumidor.join()