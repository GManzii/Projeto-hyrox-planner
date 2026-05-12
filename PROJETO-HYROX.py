treinos = []

def add():
    treino = {
        "nome": input("Nome do treino: "),
        "tipo": input("Tipo de treino: "),
        "duracao": input("Duração (em minutos): "),
        "intensidade": input("Intensidade: "),
        "data": input("Data: ")
    }

    treinos.append(treino)
    print("Treino adicionado com sucesso!\n")


def visualizar():
    if not treinos:
        print("Nenhum treino encontrado.\n")

    else:
        for i, treino in enumerate(treinos):
            print(f"\n--- {i}° treino ---")
            print(f"Nome: {treino['nome']}")
            print(f"Tipo: {treino['tipo']}")
            print(f"Duração: {treino['duracao']}")
            print(f"Intensidade: {treino['intensidade']}")
            print(f"Data: {treino['data']}")


def editar():
    visualizar()

    if not treinos:
        return

    i = int(input("\nDigite o número do treino que deseja editar: "))

    if i >= 0 and i < len(treinos):

        print("\nCampos disponíveis:")
        print("nome | tipo | duracao | intensidade | data")

        campo = input("Digite o campo que será editado: ").lower()

        if campo in treinos[i]:

            novo_valor = input("Novo valor: ")
            treinos[i][campo] = novo_valor

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
