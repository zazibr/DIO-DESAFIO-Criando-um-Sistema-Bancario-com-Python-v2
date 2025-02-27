import textwrap


def menu():
    menu: str = ("\n\n"
            "    ******************** MENU ********************\n"
            "    [d] \t  Depositar\n"
            "    [s] \t  Sacar\n"
            "    [e] \t  Extrato\n"
            "    [nc]\t  Nova Conta\n"
            "    [lc]\t  Listar Contas\n"
            "    [nu]\t  Novo Usuário\n"
            "    [q] \t  Sair\n"
            "    => ")
    return input(textwrap.dedent(menu))


def filtar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_usuario(usuarios):
    cpf: str = input("Digite o CPF (somente números: ")
    usuario = filtar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF @@@")
        return

    nome: str  = input("Digite o nome completo: ")
    data_nascimento: str = input("Digite o data de nascimento (dd-mm-aaaa): ")
    endereco: str = input("informe o endereço (logradouro, nro - bairro - cidade/uf): ")

    usuarios.append({"nome": nome,
                     "data_nascimento": data_nascimento,
                     "endereco": endereco,
                     "cpf": cpf, "endereco": endereco})

    print( "=== Usuário criado com sucesso! ===")


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input( "Informe o CPF do usuário:")
    usuario = filtar_usuario(cpf, usuarios)

    if usuario:
        print( "\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    linha = ""
    for conta in contas:
        linha = f"""\n
                Agência :\t{conta["agencia"]}
                C/C : \t{conta["numero_conta"]}
                Titular:\t{conta["usuario"]["nome"]}
                """
        print( "=" * 100)
    print(textwrap.dedent(linha))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: \t R$ {valor:.2f}\n"
        print("\n Depósito realizado com sucesso!")
    else:
        print( "@@@ Operação falou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print( "\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print( "\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print( "\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: \t R$ {valor:.2f}\n"
        numero_saques += 1
        print( "=== Saque realizado com sucesso! ===")

    else:
        print( "\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n==================== EXTRATO ====================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: {saldo:.2f}")
    print("\n=================================================")


def main():
        LIMITE_SAQUES = 3
        AGENCIA = "0001"

        saldo = 0
        limite = 500
        extrato = ""
        numero_saques = 0
        usuarios = []
        contas = []

        while True:
            opcao = menu()

            if opcao == "d":
                valor = float(input("Informe o valor do depósito: "))

                saldo, extrato = depositar(saldo, valor, extrato)

            elif opcao == "s":
                valor = float(input("Informe o valor do saque: "))
                saldo, extrato = sacar(saldo=saldo,
                                       valor=valor,
                                       extrato=extrato,
                                       limite=limite,
                                       numero_saques=numero_saques,
                                       limite_saques=LIMITE_SAQUES)

            elif opcao == "e":
                exibir_extrato(saldo, extrato=extrato)

            elif opcao == "nu":
                criar_usuario(usuarios)

            elif opcao == "nc":
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)
                
                if conta:
                    contas.append(conta)

            elif opcao == "lc":
                listar_contas(contas)

            elif opcao == "q":
                break

            else:
                print( "Operação inválida: por favor selecione novamente a operação desajada." )


main()