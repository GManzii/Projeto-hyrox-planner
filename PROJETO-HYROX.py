from datetime import datetime

treinos = []
competicoes = []
lesao_atual = None  #armazena globalmente a lesão selecionada pelo usuário


#valida e garante que a data digitada não seja futura
def obter_data_valida(mensagem="Data (DD/MM/AAAA): "):
    while True:
        data_input = input(mensagem)
        try:
            #converte o texto recebido para o formato de data (dia/mês/ano)
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y").date()
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
            data_formatada = datetime.strptime(data_input, "%d/%m/%Y").date()
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
    global lesao_atual

    nome = input(
        "Nome do exercício (sled push | sled pull | burpee broad jumps | wall balls | farmer's carry): "
    ).lower().strip()

    #mapeia exercícios que devem ser evitados para cada opção de lesão
    restricoes = {
        1: ["wall balls", "burpee broad jumps"],          # Joelho
        2: ["wall balls", "burpee broad jumps", "sled pull"], # Ombro
        3: ["burpee broad jumps", "sled push"],          # Lombar
        4: ["burpee broad jumps", "sled push", "farmer's carry"] # Panturrilha
    }

    if lesao_atual in restricoes:
        if nome in restricoes[lesao_atual]:
            print("\n[ALERTA] este é um tipo de exercício que deve ser evitado por sua lesão.\n")

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
            print("Treino updated!\n")
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

#cadastra uma competição completa coletando as informações do usuário
def cadastrar_competicao():
    print(f"\n--- Cadastrar Competição ---")

    data = obter_data_futura()
    local = input("Local da competição: ")
    categoria = input("Categoria(iniciante, intermediário ou avançado): ")

    competicao = {"data": data,"local": local,"categoria":categoria}

    competicoes.append(competicao)
    #salva no arquivo
    salvar_competicoes_txt()
    print("Competição cadastrada com sucesso!")

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
            
#acompanha a evolução entre a data mais antiga e a mais nova
def acompanhar_evolucoes(treinos):
 if not treinos:
    print(" Nenhum treino cadastrado.")
    return
 
 print("\nEVOLUÇÃO")
 print("===================================")

 # identificar em quais semanas ocorreram os treinos
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

 # Exibe a frequência semanal
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

# Percorre os treinos ordenados para obter os tempos
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

#divisão semanal ideal por nível 
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
      print("Você tem poucos treinos registrados. Foque em criar consistência (3x por semana)!")
    elif simulados == 0:
        print("Inclua pelo menos 1 simulado HYROX por semana para treinar as transições!")
    else:
        print("Boa frequência! Foque em melhorar tempos e progredir cargas aos poucos!")


#adaptação caso haja lesão
def gerenciar_lesoes():
    global lesao_atual
    print("\n============= Intervenção de lesões =============")
    print("Selecione a região onde apresenta dor, desconforto ou lesão:")
    print("[1] - Joelho")
    print("[2] - Ombro")
    print("[3] - Lombar/Coluna Vertebral")
    print("[4] - Panturrilha")
    print("[5] - Nenhuma Lesão (Limpar Histórico)")
    print("[6] - Voltar ao menu principal")
    
    try:
        opcao = int(input("\nEscolha uma opção: "))
        if opcao in [1, 2, 3, 4]:
            lesao_atual = opcao  # Atribui a lesão ativa globalmente
            
        if opcao == 1:
            print("\nPROTOCOLO RECUPERAÇÃO ATIVA: JOELHO")
            print("\nDiretriz de Treino:")
            print("  Reduzir o impacto repetitivo.")
            print("\nO que você PODE cadastrar no sistema atualmente:")
            print("  - Treino de força (focado em membros superiores)")
            print("  - Exercícios HYROX permitidos:")
            print("    * sled pull (com passos controlados para trás)")
            print("    * farmer's carry (com passos curtos e controlados)")
            print("\nO que você DEVE EVITAR cadastrar:")
            print("  - wall balls")
            print("  - burpee broad jumps")
            print("  - treino de corrida")
            
        elif opcao == 2:
            print("\nPROTOCOLO RECUPERAÇÃO ATIVA: OMBRO")
            print("\nDiretriz de treino:")
            print("  Evitar posições de impacto articular e lançamentos.")
            print("\nO que você PODE cadastrar no sistema atualmente:")
            print("  - Treino de corrida")
            print("  - Exercícios HYROX permitidos:")
            print("    * sled push (mantenha os braços esticados e firmes, empurrando com as pernas)")
            print("    * farmer's carry (melhora a estabilidade isométrica e estática do ombro)")
            print("\nO que você DEVE EVITAR cadastrar (não selecione no Simulado HYROX):")
            print("  - wall balls")
            print("  - burpee broad jumps")
            print("  - sled pull")
            
        elif opcao == 3:
            print("\nPROTOCOLO RECUPERAÇÃO ATIVA: LOMBAR")
            print("\nDiretriz de treino:")
            print("  Manutenção da coluna neutra e proteção de discos intervertebrais.")
            print("\nO que você PODE cadastrar no sistema atualmente:")
            print("  - Tipo de treino: corrida (em ritmo leve/moderado e postura ereta)")
            print("  - Exercícios HYROX permitidos:")
            print("    * farmer's carry (mantendo postura ereta e carga moderada)")
            print("    * wall balls (com coluna alinhada durante o agachamento)")
            print("\nO que você DEVE EVITAR cadastrar (não selecione no Simulado HYROX):")
            print("  - burpee broad jumps")
            print("  - sled push")
            print("  - treino de força")
        
        elif opcao == 4:
            print("\nPROTOCOLO RECUPERAÇÃO ATIVA: PANTURRILHA")
            print("\nDiretriz de Treino:")
            print("  Reduzir a força de propulsão explosiva e a sobrecarga no tendão de Aquiles.")
            print("\nO que você PODE cadastrar no sistema atualmente:")
            print("  - Tipo de treino: força (exercícios isolados de membros superiores ou tronco)")
            print("  - Exercícios HYROX permitidos:")
            print("    * wall balls (com calcanhares firmes no chão, sem estender a panturrilha no final)")
            print("    * sled pull (puxando o peso de forma controlada)")
            print("\nO que você DEVE EVITAR cadastrar (não selecione no Simulado HYROX):")
            print("  - treino de corrida")
            print("  - burpee broad jumps")
            print("  - sled push e farmer's carry")
        
        elif opcao == 5:
            lesao_atual = None
            print("\nNenhuma lesão ativa configurada no perfil.")
        elif opcao == 6:
            return
        else:
            print("Opção inválida.")
    except ValueError:
        print("Entrada inválida. Digite um número válido.")

carregar_txt()
carregar_competicoes_txt() 

#Menu Hyrox
print("============== Hyrox Planner ==============")
while True:
    print("\n[1] - Gerenciar treinos e exercícios")
    print("[2] - Visualizar treinos")
    print("[3] - Adicionar competição")
    print("[4] - Visualizar competições")
    print("[5] - Acompanhar evolução")
    print("[6] - Sugestões personalizadas")
    print("[7] - Indicar lesão (Adaptar treinos)")
    print("[8] - Sair")

    try:
        op = int(input("\nEscolha: "))
        if op == 1:
            while True:
                print("\n[1] - Adicionar treino")
                print("[2] - Editar treino")
                print("[3] - Excluir treino")
                print("[4] - Editar exercício")
                print("[5] - Excluir exercício")
                print('[6] - Voltar ao menu principal')
                num = int(input("Digite o código referente ao que deve ser feito: "))
                if num == 1:
                    add()
                elif num == 2:
                    editar()
                elif num == 3:
                    remover()
                elif num == 4:
                    editar_exercicio()
                elif num == 5:
                    remover_exercicio()
                elif num == 6:
                    break
        elif op == 2:
            visualizar()
        elif op == 3:
            cadastrar_competicao()
        elif op == 4:
            vizualizar_competicoes()
        elif op == 5:
            acompanhar_evolucoes(treinos)
        elif op == 6:
            sugestoes()
        elif op == 7:
            gerenciar_lesoes()
        elif op == 8:
            print("Programa encerrado.")
            break
        else:
            print("Erro. Número selecionado não corresponde a nenhuma ação.")
    except ValueError:
        print("Digite apenas números.")
    continue
