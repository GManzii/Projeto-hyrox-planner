
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

def obter_data_futura(mensagem="Data (DD/MM/AAAA): "):
    while True:

        data_input = input(mensagem)
        try:
            #converte o texto recebido para o formato de data (dia/mês/ano)
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y").date()
            #captura a data atual do sistema
            hoje = datetime.today().date()
           
            if data_formatada < hoje:
                print("Erro: Não é permitido cadastrar competições em datas passadas!")
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

#salva todas as competições em arquivo (uma por linha: data;local;categoria)
def salvar_competicoes_txt():
    with open("COMPETICOES.txt", "w", encoding="utf-8") as arquivo:
        for competicao in competicoes:
            linha = (
                f"{competicao['data']};"
                f"{competicao['local']};"
                f"{competicao['categoria']}\n"
            )
            arquivo.write(linha)

#lê o arquivo e reconstrói a lista de competições no sistema
def carregar_competicoes_txt():
    try:
        with open("COMPETICOES.txt", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                if linha.strip() == "":
                    continue

                dados = linha.strip().split(";")
                #ignora linha se não tiver os 3 campos esperados
                if len(dados) < 3:
                    continue

                competicao = {
                    "data": dados[0],
                    "local": dados[1],
                    "categoria": dados[2]
                }
                competicoes.append(competicao)
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
        print("Nome | Tipo | Duracao | Intensidade | Data")

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

#cadastra uma competição completa coletando as informações do usuário
def cadastrar_competicao():
    print(f"\n--- Cadastrar Competição ---")

    data = obter_data_futura()
    local = input("Local da competição: ")
    categoria = input("Categoria: ")

    comperticao = {"data": data,"local": local,"categoria":categoria}

    competicoes.append(comperticao)
    #salva no arquivo
    salvar_competicoes_txt()
    print("Competição cadastrada com sucesso!")

#acompanha a evolução entre a data mais antiga e a mais nova
def acompanhar_evolucoes(treinos):
 if not treinos:
    print(" Nenhum treino cadastrado.")
    return
 
 print("\nEVOLUÇÃO")
 print("===================================")

 total_treinos = len(treinos)
 semanas = set()
 for treino in treinos:
    data = datetime.strptime(
        treino["data"],
        "%d/%m/%Y"
    )
    semana = data.isocalendar()[1]
    semanas.add(semana)

 total_semanas = len(semanas)

 if total_semanas > 0:
    frequencia = total_treinos // total_semanas

    if total_treinos % total_semanas != 0:
        frequencia += 1
 else:
    frequencia = 0

 print(f"\n FREQUÊNCIA SEMANAL: \n {frequencia} treino(s) por semana")

 treinos_ordenados = sorted(
    treinos,
    key=lambda treino: datetime.strptime(
        treino["data"],
        "%d/%m/%Y"
    )
 )
 primeiro_tempo = None
 ultimo_tempo = None

 for treino in treinos_ordenados:
    if "duracao" in treino:
        try:
            tempo = float(treino["duracao"])

            if primeiro_tempo is None:
                primeiro_tempo = tempo
            ultimo_tempo = tempo

        except ValueError:
            pass

 print("\n EVOLUÇÃO DE TEMPOS:")

 if primeiro_tempo is not None and ultimo_tempo is not None:

    print(f" Primeiro treino: {primeiro_tempo} minutos")
    print(f" Último treino: {ultimo_tempo} minutos")

    diferenca_tempo = ultimo_tempo - primeiro_tempo

    if diferenca_tempo < 0:
     print(f" Piorou: {abs(diferenca_tempo)} minutos")
    elif diferenca_tempo > 0:
     print(f" Evoluiu: {diferenca_tempo} minutos")
    else:
     print(" Permaneceu igual")

 else:
     print(" Nenhum tempo registrado")

 primeira_carga = None
 ultima_carga = None

 for treino in treinos_ordenados:
    for exercicio in treino["exercicios"]:

        if "carga" in exercicio:
            try:
                carga = float(exercicio["carga"])

                if primeira_carga is None:
                    primeira_carga = carga

                ultima_carga = carga

            except ValueError:
                pass

 print("\n EVOLUÇÃO DE CARGAS:")

 if primeira_carga is not None and ultima_carga is not None:

    print(f" Primeiro treino: {primeira_carga} kg")
    print(f" Último treino: {ultima_carga} kg")

    diferenca_carga = ultima_carga - primeira_carga

    if diferenca_carga > 0:
     print(f" Evoluiu: {diferenca_carga} kg")
    elif diferenca_carga < 0:
     print(f" Piorou: {abs(diferenca_carga)} kg")
    else:
     print(" Permaneceu igual")

 else:
    print(" Nenhuma carga registrada")

#exibe na tela todas as competições salvas e os detalhes de cada uma
def vizualizar_competicoes():
    if not competicoes:
        print("Nenhuma competição cadastrada.\n")
    else:
        print("\n--- Competições Cadastradas ---")

        for i, competicao in enumerate(competicoes):
            data_competicao = datetime.strptime(competicao["data"], "%d/%m/%Y").date()
            hoje = datetime.today().date()
            dias_faltando = (data_competicao - hoje).days

            print(f"\n--- Ccompetição {i+1} ---")
            print(f"Data: {competicao['data']}")
            print(f"Local: {competicao['local']}")
            print(f"Categoria: {competicao['categoria']}")
            print(f"Faltam {dias_faltando} dias para o evento.")

#para gerar sugestões baseadas no nível do atleta
def sugestoes():
    print ("\n--- Sugestões Personalizadas ---")
    nivel = input("Insira o seu nível: (iniciante; intermediário; avançado ):\n").strip().lower()

    #aceita tanto com acento quanto sem acento
    if nivel == "intermediário":
        nivel = "intermediario"
    if nivel == "avançado":
        nivel = "avancado"
    
    if nivel != "iniciante" and nivel != "intermediario" and nivel != "avancado":
        print ("\nNível inválido. Escolha entre iniciante, intermediário, avançado ")
        return
    #analisar os resultados anteriores
    total_treinos = len(treinos)

    corridas = 0
    forcas = 0
    simulados = 0

    for treino in treinos:
       tipo = treino["tipo"].lower()
       if tipo == "corrida":
        corridas +=1
       elif tipo == "força":
        forcas +=1
       elif tipo == "simulado hyrox":
        simulados += 1

#armazena a maior carga atingida em cada exercicio
    maiores_cargas = {}
    for treino in treinos:
        for exercicio in treino["exercicios"]:
            if "carga" in exercicio:
                try:
                    carga = float(exercicio["carga"])
                except ValueError:
                    continue
                nome = exercicio["nome"]
                if nome not in maiores_cargas or carga > maiores_cargas[nome]:
                    maiores_cargas[nome] = carga

    print(f"\nResumo até agora: {total_treinos} treino(s) cadastrado(s).")
    print(f"Corrida: {corridas} | Força: {forcas} | Simulado HYROX: {simulados}")

# divisão semanal ideal por nível 
    divisao = {
        "iniciante": [
            "Segunda, sugestao: Corrida leve 20-30 min",
            "Quarta, sugestao: Força full body (agachamento, remada, core)",
            "Sábado, sugestao: Simulado HYROX curto (3 a 4 estações)"
        ],
        "intermediario": [
            "Segunda, sugestao: Corrida intervalada (ex: 6x400m)",
            "Terça, sugestao: Força de pernas + core",
            "Quinta, sugestao: Força de superiores + pegada (grip)",
            "Sexta, sugestao: Corrida longa contínua",
            "Sábado, sugestao: Simulado HYROX completo"
        ],
        "avancado": [
            "Segunda, sugestao: Corrida intervalada forte",
            "Terça, sugestao: Força pesada de pernas",
            "Quarta, sugestao: Transições corrida + estação (compromised running)",
            "Quinta, sugestao: Força de superiores + pegada",
            "Sexta, sugestao: Corrida longa em ritmo de prova",
            "Sábado, sugestao: Simulado HYROX completo cronometrado"
        ]
    }

    print(f"\nDivisão semanal sugerida ({nivel}):")
    for dia in divisao[nivel]:
        print(f"- {dia}")

# cargas ideais por nível; se já houver registro, sugere progressão de 5% 
    cargas_base = {
        "iniciante": {"sled push": 50, "sled pull": 50, "wall balls": 4, "farmer's carry": 16},
        "intermediario": {"sled push": 75, "sled pull": 75, "wall balls": 6, "farmer's carry": 20},
        "avancado": {"sled push": 100, "sled pull": 100, "wall balls": 9, "farmer's carry": 24}
    }
    print(f"\nCargas ideais sugeridas  para ({nivel}):")
    for exercicio_nome, carga_base in cargas_base[nivel].items():
        if exercicio_nome in maiores_cargas:
            atual = maiores_cargas[exercicio_nome]
            meta = round(atual * 1.05, 1)
            print(f"- {exercicio_nome}: você já fez {atual} kg, tente progredir para {meta} kg")
        else:
            print(f"- {exercicio_nome}: comece com cerca de {carga_base} kg")

 #estratégias por etapa do HYROX 
    print("\nEstratégias por etapa do HYROX:")
    print("- Corrida: mantenha ritmo constante, não comece rápido demais")
    print("- Sled push/pull: passos curtos e fortes, tronco firme")
    print("- Burpee broad jumps: economize energia, salto controlado")
    print("- Wall balls: respiração  ritmada e mire sempre no mesmo ponto")
    print("- Farmer's carry: pegada firme, ombros para trás e passo constante")

# dica geral com base na frequência de treinos 
    print("\nDica geral:")
    if total_treinos < 3:
      print("Você tem poucos treinos registrados. Foque em criar consistência (3x por semana).")
    elif simulados == 0:
        print("Inclua pelo menos 1 simulado HYROX por semana para treinar as transições.")
    else:
        print("Boa frequência! Foque em melhorar tempos e progredir cargas aos poucos.")

carregar_txt()
carregar_competicoes_txt() 

#Menu Hyrox
print("============== Hyrox Planner ==============")
while True:
    print("\n[1] - Gerenciar treinos")
    print("[2] - Visualizar treinos e exercícios")
    print("[3] - Gerenciar exercícios")
    print("[4] - Gerenciar competições")
    print("[5] - Sugestões personalizadas")
    print("[6] - Acompanhar evolução")
    print("[7] - Sair")

    try:
        op = int(input("\nEscolha: "))

        if op == 1:
            print("\n[1] - Adicionar treino")
            print("[2] - Editar treino")
            print("[3] - Excluir treino")
            try:
                optreino = int(input("\nEscolha: "))
                if optreino == 1:
                    add()
                elif optreino == 2:
                    editar()
                elif optreino == 3:
                    remover()
                else:
                    print("Opção inválida")
                continue
            except ValueError:
                print("Digite apenas números.")

        elif op == 2:
            visualizar()

        elif op == 3:
            print("[1] - Editar exercício")
            print("[2] - Excluir exercício")
            try:
                opexer = int(input("\nEscolha: "))
                if opexer == 1:
                    editar_exercicio()
                elif opexer == 2:
                    remover_exercicio()
                else:
                    print("Opção inválida")
                continue
            except ValueError:
                print("Digite apenas números.")
        elif op == 4:
            print("[1] - Adicionar competição")
            print("[2] - Visualizar competições")
            try:
                opexer = int(input("\nEscolha: "))
                if opexer == 1:
                    cadastrar_competicao()
                elif opexer == 2:
                    vizualizar_competicoes()
                else:
                    print("Opção inválida")
                continue
            except ValueError:
                print("Digite apenas números.")
        elif op == 5:
            sugestoes()
        elif op == 6:
            acompanhar_evolucoes(treinos)
        elif op == 7:
            print("Programa encerrado.")
            break
        else:
            print("Erro. Número selecionado não corresponde a nenhuma ação.")
    except ValueError:
        #captura erros de digitação caso o usuário insira letras no menu
        print("Digite apenas números.")
    continue
