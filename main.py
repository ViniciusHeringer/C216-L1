alunos = []
contadores_cursos = {}


def gerar_matricula(curso):
    curso = curso.upper()
    if curso not in contadores_cursos:
        contadores_cursos[curso] = 1
    else:
        contadores_cursos[curso] += 1

    return f"{curso}{contadores_cursos[curso]}"


def criar_aluno():
    print("\nCadastro Aluno")
    nome = input("Nome: ")
    email = input("Email: ")
    curso = input("Curso: ").upper()

    matricula = gerar_matricula(curso)

    novo_aluno = {
        "nome": nome,
        "email": email,
        "curso": curso,
        "matricula": matricula
    }

    alunos.append(novo_aluno)
    print(f"\nAluno cadastrado com sucesso. Matrícula: {matricula}")


def listar_alunos():
    print("\nLista Alunos")
    if not alunos:
        print("Nenhum aluno cadastrado")
        return

    for aluno in alunos:
        print(
            f"Matrícula: {aluno['matricula']} | Nome: {aluno['nome']} | Curso: {aluno['curso']} | Email: {aluno['email']}")


def atualizar_aluno():
    print("\nAtualiza Aluno")
    matricula = input("Digite a matrícula do aluno que deseja alterar: ").upper()

    for aluno in alunos:
        if aluno['matricula'] == matricula:
            print(f"Editando dados de: {aluno['nome']}")
            aluno['nome'] = input(f"Novo nome (atual: {aluno['nome']}): ") or aluno['nome']
            aluno['email'] = input(f"Novo email (atual: {aluno['email']}): ") or aluno['email']
            print("Dados atualizados")
            return

    print("Aluno nao encontrado")


def excluir_aluno():
    print("\nApaga Aluno")
    matricula = input("Digite a matrícula do aluno que deseja remover: ").upper()

    for aluno in alunos:
        if aluno['matricula'] == matricula:
            alunos.remove(aluno)
            print(f"Aluno {matricula} removido com sucesso.")
            return

    print("Aluno não encontrado")


def menu():
    while True:
        print("\n=== SISTEMA ACADÊMICO ===")
        print("1- Cadastrar Aluno")
        print("2- Listar Alunos")
        print("3- Atualizar Aluno")
        print("4- Excluir Aluno")
        print("5- Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            criar_aluno()
        elif opcao == '2':
            listar_alunos()
        elif opcao == '3':
            atualizar_aluno()
        elif opcao == '4':
            excluir_aluno()
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()