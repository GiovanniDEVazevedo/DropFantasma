# =========================
# menus.py
# MENU TERMINAL
# =========================

from utils import criar_save, ler_save
import webbrowser

URL_MVP = "https://dropfantasma.onrender.com"


def calcular_status():
    dados = ler_save()
    total = dados["pontos"]
    passagens = total // 120
    sobra = total % 120
    return total, passagens, sobra


def abrir_mvp():
    print("\nAbrindo Soul Hunter Web...")
    webbrowser.open(URL_MVP)


def mostrar_colecao():
    dados = ler_save()
    print("\n=========== COLEÇÃO ===========")
    if not dados["colecao"]:
        print("Nenhum fantasma capturado.")
    else:
        for i, fantasma in enumerate(dados["colecao"], 1):
            qtd = fantasma.get("quantidade", 1)
            print(
                f"{i}. {fantasma['nome']} "
                f"- {fantasma['raridade']} "
                f"(x{qtd})"
            )
    print("================================")


def mostrar_extrato():
    total, passagens, sobra = calcular_status()
    print("\n=========== CARTEIRA ===========")
    print(f"Saldo total: {total}")
    print(f"Passagens disponíveis: {passagens}")
    if sobra == 0 and total > 0:
        print("Passagem completa!")
    else:
        print(f"Faltam {120 - sobra} pontos")
    print("================================")


def ler_opcao():
    while True:
        entrada = input("> ")
        if entrada.isdigit():
            return int(entrada)
        print("Digite apenas números.")


def carteira_menu():
    while True:
        print("\n=========== CARTEIRA ===========")
        print("1. Ver extrato")
        print("2. Voltar")
        opcao = ler_opcao()
        if opcao == 1:
            mostrar_extrato()
        elif opcao == 2:
            break
        else:
            print("Opção inválida")


def menu_soul():
    while True:
        dados = ler_save()
        print("\n=========== SOUL HUNTER ===========")
        print(
            f"Fantasmas capturados: "
            f"{len(dados['colecao'])}"
        )
        print("\n1. Abrir captura web")
        print("2. Ver coleção")
        print("3. Voltar")
        opcao = ler_opcao()
        if opcao == 1:
            abrir_mvp()
        elif opcao == 2:
            mostrar_colecao()
        elif opcao == 3:
            break
        else:
            print("Opção inválida")


def menu_principal():
    while True:
        print("\n=========== SOUL UP ===========")
        print("1. Carteira")
        print("2. Soul Hunter")
        print("3. Sair")
        opcao = ler_opcao()
        if opcao == 1:
            carteira_menu()
        elif opcao == 2:
            menu_soul()
        elif opcao == 3:
            print("\nSaindo...")
            break
        else:
            print("Opção inválida")


if __name__ == "__main__":
    criar_save()
    menu_principal()
