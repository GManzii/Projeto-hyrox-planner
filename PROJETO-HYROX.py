treinos = []
exercicios = []

def salvar_txt():

    with open("HYROX.txt", "w", encoding="utf-8") as arquivo:

        for treino in treinos:

            linha = f"{treino['nome']};{treino['tipo']};{treino['duracao']};{treino['intensidade']};{treino['data']}\n"

            arquivo.write(linha)

def carregar_txt():

    try:

        with open("HYROX.txt", "r", encoding="utf-8") as arquivo:

            for linha in arquivo:

                dados = linha.strip().split(";")

                treino = {
                    "nome": dados[0],
                    "tipo": dados[1],
                    "duracao": dados[2],
                    "intensidade": dados[3],
                    "data": dados[4]
                }

                treinos.append(treino)

    except FileNotFoundError:
        pass
def add_exercicio():
    exercicio = {
        "nome": input("Nome do exercício: "),
        "tempo": input("Tempo: "),
        "distancia": input("Distância: "),
        "carga": input("Carga: "),
        "repeticoes": input("Repetições: ")
    }
    exercicios.append(exercicio)
    print("Exercício adicionado com sucesso!\n")
    
def add():
    treino = {
        "nome": input("Nome do treino: "),
        "tipo": input("Tipo de treino (corrida | força | simulado hyrox): "),
        "duracao": input("Duração (em minutos): "),
        "intensidade": input("Intensidade (baixa | moderada | alta) : "),
        "data": input("Data: ")
    }

    treinos.append(treino)

    if treino["tipo"].lower == "simulado hyrox":
        qtd = input("Quantos exercícios de Hyrox deseja adicionar: ")
        for i in range(qtd):
            print(f"\n--- {i+1}° exercício ---")
            add_exercicio()

    print("Treino adicionado com sucesso!\n")


def visualizar():
    if not treinos:
        print("Nenhum treino encontrado.\n")

    else:
        for i, treino in enumerate(treinos):
            print(f"\n--- {i+1}° treino ---")
            print(f"Nome: {treino['nome']}")
            print(f"Tipo: {treino['tipo']}")
            print(f"Duração: {treino['duracao']} minutos")
            print(f"Intensidade: {treino['intensidade']}")
            print(f"Data: {treino['data']}")


def editar():
    visualizar()

    if not treinos:
        return

    i = int(input("\nDigite o número do treino que deseja editar: "))

    if i-1 >= 0 and i-1 < len(treinos):

        print("\nCampos disponíveis:")
        print("nome | tipo | duracao | intensidade | data")

        campo = input("Digite o campo que será editado: ").lower()

        if campo in treinos[i-1]:

            novo_valor = input("Novo valor: ")
            treinos[i-1][campo] = novo_valor

            print("Treino atualizado!\n")

        else:
            print("Campo inválido.\n")

    else:
        print("Treino não encontrado.\n")


def remover():
    visualizar()

    if not treinos:
        return

    t = int(input("\nQual treino deseja remover: "))

    if t >= 0 and t < len(treinos):

        treinos.pop(t)
        print("Treino removido!\n")

    else:
        print("Treino não encontrado.\n")

carregar_txt()
print("============= HYROX Planner ============= ")

while True:

    print("\n1 - Adicionar")
    print("2 - Visualizar")
    print("3 - Editar")
    print("4 - Excluir")
    print("5 - Parar")

    op = int(input("\nEscolha: "))

    if op == 1:
        add()

    elif op == 2:
        visualizar()

    elif op == 3:
        editar()

    elif op == 4:
        remover()

    elif op == 5:
        print("Programa encerrado.")
        break

    else:
        print("Erro. Número selecionado não corresponde a nenhuma ação.")
    
