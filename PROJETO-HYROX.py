treinos = []

def add():
    tipo = input("Tipo de treino: ")
    duracao = input("Duração: ")
    intensidade = input("Intensidade: ")
    data = input("Data: ")
    treino = [tipo,duracao,intensidade,data]
    treinos.append()
    return add

print("============= Hyrox Planner ============= ")

while True:
    print("1-adicionar\n2-visualizar\n3-editar\n4-excluir")
    op = int(input("Escolha: "))
    if op == 1:
        add()
