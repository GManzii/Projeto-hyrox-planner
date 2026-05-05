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

print("============= Hyrox Planner ============= ")
print("1-adicionar\n2-visualizar\n3-editar\n4-excluir\n5-excluir")
while True:
    
    op = int(input("Escolha: "))
    if op == 1:
        add()
    elif op == 2:
        vizualizar()
