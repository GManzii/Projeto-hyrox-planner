treinos = []

def add():
    treino = {
        "tipo": input("Tipo de treino: "),
        "duracao": input("Duração: "),
        "intensidade": input("Intensidade: "),
        "data": input("Data: ")
    }
    treinos.append(treino)
def vizualizar():
    if not treinos:
        print("nenhum treino encontrado")
    else:
        for i, treino in enumerate(treinos):
            print(f"---{i}° treino---")
            print(f"tipo: {treino['tipo']}")
            print(f"duração: {treino['duracao']}")
            print(f"intensidade: {treino['intensidade']}")
            print(f"data: {treino['data']}")
def editar():
    i=int(input("qual treino você deseja editar: "))
    print("tipo/duração/intensidade/data")
    campo=(input("qual campo deseja editar: "))

    if campo in treinos[i]:
        novo_valor=input("novo valor: ")
        treinos[i][campo]=novo_valor
    else:
        print("opção inválida")
def remover():
    if not treinos:
        print("treino não encontrado")
    else:
        t=int(input("qual treino você deseja remover: "))
        treinos.pop(t)

print("============= Hyrox Planner ============= ")
print("1-adicionar\n2-visualizar\n3-editar\n4-excluir\n5-parar")
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
