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
print("1-adicionar\n2-visualizar\n3-editar\n4-excluir\n5-excluir")
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
    elif op==3:
        if len(treinos) == 0:
            print("Nenhum treino cadastrado")
        else:
            for i in range(len(treinos)):
                print(f"{i} - {treinos[i]}")

        indice = int(input("Qual treino deseja editar: "))

        print("0-tipo\n1-duração\n2-intensidade\n3-data")
        campo = int(input("Digite o campo: "))

        novo_valor = input("Novo valor: ")

        if campo == 0:
            treinos[indice] = novo_valor
        elif campo == 1:
            duracoes[indice] = novo_valor
        elif campo == 2:
            intensidades[indice] = novo_valor
        elif campo == 3:
            datas[indice] = novo_valor
        else:
            print("Campo inválido")
    elif op==4:
        valor=input()
        treinos.remove(valor)
    elif op==5:
        break
    else:
        print("opção inválida")
