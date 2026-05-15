# =========================
# main.py
# MENU TERMINAL
# =========================

import json
import os
import webbrowser

ARQUIVO_JSON = "jogador.json"

URL_MVP = "https://SEU-APP.onrender.com"


# =========================
# CRIAR SAVE
# =========================

def criar_save():

    if not os.path.exists(ARQUIVO_JSON):

        dados = {

            "colecao": [],

            "pontos": 0
        }

        with open(
            ARQUIVO_JSON,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )


# =========================
# LER SAVE
# =========================

def ler_save():

    with open(
        ARQUIVO_JSON,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)


# =========================
# CALCULAR STATUS
# =========================

def calcular_status():

    dados = ler_save()

    total = dados["pontos"]

    passagens = total // 120

    sobra = total % 120

    return total, passagens, sobra


# =========================
# ABRIR MVP WEB
# =========================

def abrir_mvp():

    print("\nAbrindo Soul Hunter Web...")

    webbrowser.open(URL_MVP)


# =========================
# MOSTRAR COLEÇÃO
# =========================

def mostrar_colecao():

    dados = ler_save()

    print("\n=========== COLEÇÃO ===========")

    if not dados["colecao"]:

        print("Nenhum fantasma capturado.")

    else:

        for i, fantasma in enumerate(
            dados["colecao"], 1
        ):

            print(
                f"{i}. "
                f"{fantasma['nome']} "
                f"- {fantasma['raridade']}"
            )

    print("================================")


# =========================
# EXTRATO
# =========================

def mostrar_extrato():

    total, passagens, sobra = calcular_status()

    print("\n=========== CARTEIRA ===========")

    print(f"Saldo total: {total}")

    print(f"Passagens disponíveis: {passagens}")

    print(f"Faltam {120 - sobra} pontos")

    print("================================")


# =========================
# VALIDAR MENU
# =========================

def ler_opcao():

    while True:

        entrada = input("> ")

        if entrada.isdigit():

            return int(entrada)

        print("Digite apenas números.")


# =========================
# MENU CARTEIRA
# =========================

def carteira_menu():

    while True:

        print("\n=========== CARTEIRA ===========")

        print("1. Ver extrato")
        print("2. Voltar")

        opcao = ler_opcao()

        match opcao:

            case 1:

                mostrar_extrato()

            case 2:

                break

            case _:

                print("Opção inválida")


# =========================
# MENU SOUL HUNTER
# =========================

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

        match opcao:

            case 1:

                abrir_mvp()

            case 2:

                mostrar_colecao()

            case 3:

                break

            case _:

                print("Opção inválida")


# =========================
# MENU PRINCIPAL
# =========================

def menu_principal():

    while True:

        print("\n=========== SOUL UP ===========")

        print("1. Carteira")
        print("2. Soul Hunter")
        print("3. Sair")

        opcao = ler_opcao()

        match opcao:

            case 1:

                carteira_menu()

            case 2:

                menu_soul()

            case 3:

                print("\nSaindo...")

                break

            case _:

                print("Opção inválida")


# =========================
# START
# =========================

criar_save()

menu_principal()