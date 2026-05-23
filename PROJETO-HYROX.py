#importa o módulo para manipulação de datas
from datetime import datetime

treinos = []
competicoes = []

#valida e garante que a data digitada não seja futura
def obter_data_valida(mensagem="Data (DD/MM/AAAA): "):
    while True:

        data_input = input(mensagem)
        try:
            #converte o texto recebido para o formato de data (dia/mês/ano)
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y").date()
            #captura a data atual do sistema
            hoje = datetime.today().date()
            
            if data_formatada > hoje:
                print("Erro: Não é permitido cadastrar treinos em datas futuras!")
            else:
                return data_input 
        except ValueError:
            print("Erro: Formato de data inválido! Use o formato DD/MM/AAAA (Ex: 15/05/2024).")

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

#lê o arquivo e reconstrói a lista de treinos no sistema
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

                #verifica se a linha lida possui a seção interna de exercícios cadastrados
                if len(dados) > 5 and dados[5] != "":

                    lista_exercicios = dados[5].split("|")
                    for exercicio_txt in lista_exercicios:
                        exercicio = {}
                        atributos = exercicio_txt.split(",")
                        for atributo in atributos:
                            chave, valor = atributo.split("=")
                            exercicio[chave] = valor
                        treino["exercicios"].append(exercicio)

                treinos.append(treino)
    except FileNotFoundError:
        pass

#adiciona novo exercício e seus dados dentro de um treino
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

#cadastra um treino completo coletando as informações do usuário
def add():
    treino = {
        "nome": input("Nome do treino: "),
        "tipo": input("Tipo de treino (corrida | força | simulado hyrox): "),
        "duracao": input("Duração (em minutos): "),
        "intensidade": input("Intensidade (baixa | moderada | alta): "),
        "data": obter_data_valida("Data (DD/MM/AAAA): "), 
        "exercicios": []
    }

    if treino["tipo"].lower() == "simulado hyrox":
        qtd = int(input("Quantos exercícios de Hyrox deseja adicionar: "))
        for i in range(qtd):
            print(f"\n----- {i+1}° exercício -----")
            add_exercicio(treino)

    elif treino["tipo"].lower() != "força" and treino["tipo"].lower() != "corrida":
        print("Tipo inválido")
        return

    treinos.append(treino)
    salvar_txt()
    print("Treino adicionado com sucesso!\n")

#exibe na tela todos os treinos salvos e seus respectivos detalhes/exercícios
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

            #lista todos os dados dos sub-exercícios
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

#edita um treino selecionado pelo usuário
def editar():
    visualizar()
    if not treinos:
        return

    i = int(input("\nDigite o número do treino que deseja editar: "))

    if i-1 >= 0 and i-1 < len(treinos):
        print("\nCampos disponíveis:")
        print("Nome | Tipo | Duração | Intensidade | Data")

        campo = input("Digite o campo que será editado: ").lower()

        if campo in treinos[i-1]:
            if campo == "data":
                novo_valor = obter_data_valida("Novo valor para Data (DD/MM/AAAA): ")
            else:
                novo_valor = input("Novo valor: ")

            treinos[i-1][campo] = novo_valor
            
            #cadastro de exercícios caso a nova categoria mude o tipo para simulado hyrox
            if campo == "tipo" and novo_valor == "simulado hyrox":
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

def remover_exercicio():
    visualizar()
    if not treinos:
        return

    treino_indice = int(input("\nDigite o número do treino: "))

    if treino_indice-1 < 0 or treino_indice-1 >= len(treinos):
        print("Treino não encontrado.")
        return

    treino = treinos[treino_indice-1]

    if len(treino["exercicios"]) == 0:
        print("Esse treino não possui exercícios.")
        return

    print("\nExercícios:")
    for i, exercicio in enumerate(treino["exercicios"]):
        print(f"[{i+1}] - {exercicio['nome']}")

    exercicio_indice = int(input("\nDigite o número do exercício que deseja remover: "))

    if exercicio_indice-1 < 0 or exercicio_indice-1 >= len(treino["exercicios"]):
        print("Exercício não encontrado.")
        return

    treino["exercicios"].pop(exercicio_indice-1)
    salvar_txt()
    print("Exercício removido com sucesso!")

def editar_exercicio():
    visualizar()
    if not treinos:
        return

    treino_indice = int(input("\nDigite o número do treino: "))

    if treino_indice-1 < 0 or treino_indice-1 >= len(treinos):
        print("Treino não encontrado.")
        return

    treino = treinos[treino_indice-1]

    if len(treino["exercicios"]) == 0:
        print("Esse treino não possui exercícios.")
        return

    print("\nExercícios:")
    for i, exercicio in enumerate(treino["exercicios"]):
        print(f"[{i+1}] - {exercicio['nome']}")

    exercicio_indice = int(input("\nDigite o número do exercício: "))
    
    if exercicio_indice-1 < 0 or exercicio_indice-1 >= len(treino["exercicios"]):
        print("Exercício não encontrado.")
        return

    exercicio = treino["exercicios"][exercicio_indice-1]
    print("\nCampos disponíveis:")

    for chave in exercicio:
        if chave != "nome":
            print(chave)

    campo = input("\nDigite o campo que deseja editar: ")

    if campo in exercicio:
        novo_valor = input("Novo valor: ")
        exercicio[campo] = novo_valor
        salvar_txt()
        print("Exercício atualizado!")
    else:
        print("Campo inválido.")

carregar_txt()

#cadastra uma competição completa coletando as informações do usuário
def cadastrar_competicao():
    print(f"\n--- Cadastrar Competição ---")

    data = obter_data_valida()
    local = input("Local da competição: ")
    categoria = input("Categoria: ")

    comperticao = {"data": data,"local": local,"categoria":categoria}

    competicoes.append(comperticao)
    print("Competição cadastrada com sucesso!")


#exibe na tela todas as competições salvas e os detalhes de cada uma
def vizualizar_competicoes():
    if not competicoes:
        print("Nenhuma competição cadastrada.\n")
    else:
        print("\n--- Competições Cadastradas ---")

        for i, competicao in enumerate(competicoes):
            data_competicao = datetime.strptime(competicao["data"], "%d/%m/%y").date()
            hoje = datetime.today().date
            dias_faltando = (data_competicao - hoje).days

            print(f"\n--- Ccompetição {i} ---")
            print(f"Data: {competicao['data']}")
            print(f"Local: {competicao['local']}")
            print(f"Categoria: {competicao['categoria']}")
            print(f"Faltam {dias_faltando} dias para o evento.")

#Menu Hyrox
print("============== Hyrox Planner ==============")
while True:
    print("\n[1] - Adicionar treino")
    print("[2] - Visualizar treinos")
    print("[3] - Editar treino")
    print("[4] - Excluir treino")
    print("[5] - Editar exercício")
    print("[6] - Excluir exercício")
    print("[7] - Adicionar competição")
    print("[8] - Visualizar competições")
    print("[9] - Sair")

    try:
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
            editar_exercicio()
        elif op == 6:
            remover_exercicio()
        elif op == 7 :
            cadastrar_competicao()
        elif op == 8:
            vizualizar_competicoes()
        elif op == 9:
            print("Programa encerrado.")
            break
        else:
            print("Erro. Número selecionado não corresponde a nenhuma ação.")
    except ValueError:
        #captura erros de digitação caso o usuário insira letras no menu
        print("Digite apenas números.")
    continue
