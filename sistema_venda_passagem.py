import threading
from queue import Queue

# Dicionário de assentos disponíveis por data
assentos_disponiveis_por_data = {
    "20/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "22/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "25/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "27/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "29/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "01/09/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "03/09/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"]
}

# Lock para garantir que várias threads não alterem os dados ao mesmo tempo
bloqueio = threading.Lock()
request_queue = Queue()

def processar_requisicoes():
    """Função que processa requisições da fila."""
    while True:
        client_name, escolha_do_cliente, assento_escolhido = request_queue.get()
        if client_name is None:
            break
        
        # Processar escolha de data
        with bloqueio:
            if escolha_do_cliente in assentos_disponiveis_por_data:
                print(f"Cliente {client_name} escolheu a data: {escolha_do_cliente}")
                if assento_escolhido in assentos_disponiveis_por_data[escolha_do_cliente]:
                    assentos_disponiveis_por_data[escolha_do_cliente].remove(assento_escolhido)
                    print(f"Assento {assento_escolhido} reservado com sucesso para {client_name}!")
                    
                    comprovante = f"""
                    Comprovante de viagem:
                    Nome do cliente: {client_name}
                    Data da viagem: {escolha_do_cliente}
                    Assento: {assento_escolhido}
                    """
                    print(comprovante)
                else:
                    print(f"Assento {assento_escolhido} não está disponível.")
            else:
                print(f"Data {escolha_do_cliente} não está disponível.")
        request_queue.task_done()

def sistema_venda_passagem():
    """Simula o sistema de venda de passagens, interagindo diretamente com o usuário."""
    while True:
        client_name = input("Digite seu nome ou 'sair' para encerrar: ")
        if client_name.lower() == 'sair':
            request_queue.put((None, None, None))  # Sinalizar o fim das requisições
            break

        print("Datas de viagens disponíveis:")
        for data in assentos_disponiveis_por_data.keys():
            print(data)

        escolha_do_cliente = input("Escolha a data da viagem: ")
        print(f"Assentos disponíveis para {escolha_do_cliente}:")
        if escolha_do_cliente in assentos_disponiveis_por_data:
            print(", ".join(assentos_disponiveis_por_data[escolha_do_cliente]))

        assento_escolhido = input("Escolha o assento: ")

        # Colocar a requisição na fila
        request_queue.put((client_name, escolha_do_cliente, assento_escolhido))

if __name__ == "__main__":
    # Iniciar a thread que processa as requisições
    threading.Thread(target=processar_requisicoes, daemon=True).start()

    # Iniciar o sistema de venda de passagens
    sistema_venda_passagem()

    # Esperar até que todas as requisições sejam processadas
    request_queue.join()
    print("Sistema encerrado.")