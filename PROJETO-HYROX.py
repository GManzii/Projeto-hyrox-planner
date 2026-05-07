treinos = []

def add():
    treino = {
        "tipo": input("Tipo de treino: "),
        "duracao": input("Duração(em minutos): "),
        "intensidade": input("Intensidade: "),
        "data": input("Data: ")
    }
    treinos.append(treino)
def vizualizar():
    if not treinos:
        print("Nenhum treino encontrado")
    else:
        for i, treino in enumerate(treinos):
            print(f"---{i}° treino---")
            print(f"tipo: {treino['tipo']}")
            print(f"duração: {treino['duracao']}")
            print(f"intensidade: {treino['intensidade']}")
            print(f"data: {treino['data']}")
def editar():
    i=int(input("Digite o treino o qual você deseja editar: "))
    print("Tipo/duração/intensidade/data")
    campo=(input("Digite o campo que será editado: "))

    if campo in treinos[i]:
        novo_valor=input("novo valor: ")
        treinos[i][campo]=novo_valor
    else:
        print("opção inválida")
def remover():
    if not treinos:
        print("Treino não encontrado")
    else:
        t=int(input("Qual treino você deseja remover: "))
        treinos.pop(t)

print("============= Hyrox Planner ============= ")
print("1-Adicionar\n2-Visualizar\n3-Editar\n4-Excluir\n5-Parar")
while True:
    
    op = int(input("Escolha: "))
    if op == 1:
        add()
    elif op == 2:
        vizualizar()
    elif op == 3:
        editar()
    elif op == 4:
        remover()
    elif op ==5:
        break
    else:
        print("Erro. Número selecionado não corresponde a nenhuma ação.")
