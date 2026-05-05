treinos = []
duracoes = []
intensidades = []
datas = []

def add():
    tipo = input("Tipo de treino: ")
    treinos.append(tipo)
    duracao = input("Duração: ")
    duracoes.append(duracao)
    intensidade = input("Intensidade: ")
    intensidades.append(intensidade)
    data = input("Data: ")
    datas.append(data)


print("============= Hyrox Planner ============= ")
print("1-adicionar\n2-visualizar\n3-editar\n4-excluir")
while True:
    
    op = int(input("Escolha: "))
    if op == 1:
        add()
    elif op == 2:
        if len(treinos) > 0:
            for i in range(len(treinos)):
                print()
                print("---treino---")
                print(f"Treino: {treinos[i]}")
                print(f"Duração: {duracoes[i]}")
                print(f"Intensidade: {intensidades[i]}")
                print(f"Data: {datas[i]}")
                print("-----")
        else:
            print("Nenhum treino cadastrado")
