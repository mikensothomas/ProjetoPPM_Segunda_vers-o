from threading import Thread, Lock
import json
import queue

Lock = Lock()

dados = {"id": 1, "Mensagem": "exemplo"}
json_dados = json.dumps(dados)  #uma string JSON

fila = queue.Queue()

fila.put(json_dados)

dados_recebidos = fila.get()
fila.task_done()

def consumidor():
    with Lock:
        # Seção crítica (acesso à fila)
        if not fila.empty():
            dados = fila.get()
            fila.task_done()
            print(f"ados consumidos: {dados}")

thread1 = Thread(target=consumidor)
thread2 = Thread(target=consumidor)
thread1.start()
thread2.start()
