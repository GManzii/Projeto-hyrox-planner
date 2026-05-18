treinos = []

def salvar_txt():

    with open("HYROX.txt", "w", encoding="utf-8") as arquivo:

        for treino in treinos:

            lista_exercicios = []

            for exercicio in treino["exercicios"]:

                atributos = []

                for chave, valor in exercicio.items():

                    atributos.append(f"{chave}={valor}")

                exercicio_txt = ",".join(atributos)

                lista_exercicios.append(exercicio_txt)

            exercicios_txt = "|".join(lista_exercicios)

            linha = (
                f"{treino['nome']};"
                f"{treino['tipo']};"
                f"{treino['duracao']};"
                f"{treino['intensidade']};"
                f"{treino['data']};"
                f"{exercicios_txt}\n"
            )

            arquivo.write(linha)
def carregar_txt():

    try:

        with open("HYROX.txt", "r", encoding="utf-8") as arquivo:

            for linha in arquivo:

                if linha.strip() == "":
                    continue

                dados = linha.strip().split(";")

                treino = {

                    "nome": dados[0],
                    "tipo": dados[1],
                    "duracao": dados[2],
                    "intensidade": dados[3],
                    "data": dados[4],
                    "exercicios": []
                }

                treinos.append(treino)

    except FileNotFoundError:

        pass

def add_exercicio(treino):

    nome = input(
        "Nome do exercício (sled push | sled pull | burpee broad jumps | wall balls | farmer's carry): "
    ).lower()

    exercicio = {
        "nome": nome
    }

    if nome == "sled push" or nome == "sled pull":

        exercicio["tempo"] = input("Tempo (em minutos): ")
        exercicio["distancia"] = input("Distância (em metros): ")
        exercicio["carga"] = input("Carga (em kg): ")

    elif nome == "burpee broad jumps":

        exercicio["tempo"] = input("Tempo (em minutos): ")
        exercicio["distancia"] = input("Distância (em metros): ")

    elif nome == "wall balls":

        exercicio["tempo"] = input("Tempo (em minutos): ")
        exercicio["carga"] = input("Carga (em kg): ")
        exercicio["repeticoes"] = input("Repetições: ")

    elif nome == "farmer's carry":

        exercicio["tempo"] = input("Tempo (em minutos): ")
        exercicio["distancia"] = input("Distância (em metros): ")
        exercicio["carga"] = input("Carga (em kg): ")

    else:

        print("Exercício inválido.")
        return

    treino["exercicios"].append(exercicio)

    print("Exercício adicionado com sucesso!\n")

def add():

    treino = {
        "nome": input("Nome do treino: "),
        "tipo": input("Tipo de treino (corrida | forca | simulado hyrox): "),
        "duracao": input("Duração (em minutos): "),
        "intensidade": input("Intensidade (baixa | moderada | alta): "),
        "data": input("Data: "),
        "exercicios": []
    }

    if treino["tipo"].lower() == "simulado hyrox":

        qtd = int(input("Quantos exercícios de Hyrox deseja adicionar: "))

        for i in range(qtd):

            print(f"\n----- {i+1}° exercício -----")

            add_exercicio(treino)

    elif treino["tipo"].lower() != "forca" and treino["tipo"].lower() != "corrida":
        print("Tipo inválido")
        return

    treinos.append(treino)
    salvar_txt()

    print("Treino adicionado com sucesso!\n")

def visualizar():

    if not treinos:

        print("Nenhum treino cadastrado.\n")

    else:

        for i, treino in enumerate(treinos):

            print(f"\n----- {i+1}° treino -----")
            print(f"Nome: {treino['nome']}")
            print(f"Tipo: {treino['tipo']}")
            print(f"Duração: {treino['duracao']} minutos")
            print(f"Intensidade: {treino['intensidade']}")
            print(f"Data: {treino['data']}")

            if len(treino["exercicios"]) > 0:

                print("\nExercícios:")

                for exercicio in treino["exercicios"]:
                    print(f"\n- {exercicio['nome']}")
                    if "tempo" in exercicio:
                        print(f"  Tempo: {exercicio['tempo']} minutos")

                    if "distancia" in exercicio:
                        print(f"  Distância: {exercicio['distancia']} metros")

                    if "carga" in exercicio:
                        print(f"  Carga: {exercicio['carga']} kg")

                    if "repeticoes" in exercicio:
                        print(f"  Repetições: {exercicio['repeticoes']}")

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
            if novo_valor == "simulado hyrox":

                qtd = int(input("Quantos exercícios de Hyrox deseja adicionar: "))

                for j in range(qtd):

                    print(f"\n----- {j+1}° exercício -----")

                    add_exercicio(treinos[i-1])

                salvar_txt()

                print("Treino atualizado!\n")

        else:
            print("Campo inválido.\n")

    else:
        print("Treino não encontrado.\n")

def remover():

    visualizar()

    if not treinos:
        return

    t = int(input("\nDigite o número do treino que deseja remover: "))

    if t-1 >= 0 and t-1 < len(treinos):

        treinos.pop(t-1)
        salvar_txt()

        print("Treino removido!\n")

    else:
        print("Treino não encontrado.\n")

carregar_txt()
print("============== Hyrox Planner ==============")


while True:

    print("\n[1] - Adicionar treino")
    print("[2] - Visualizar treinos")
    print("[3] - Editar treino")
    print("[4] - Excluir treino")
    print("[5] - Sair")

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
