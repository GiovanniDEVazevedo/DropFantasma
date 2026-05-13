from flask import Flask, jsonify, render_template
import random
import json
import os

app = Flask(__name__)

# =========================
# BANCO DE FANTASMAS
# =========================

banco_de_fantasmas = [
    {
        "id": 1,
        "nome": "Fantasma Comum",
        "raridade": "Comum",
        "chance": 50,
        "urlImagem": "/static/img/fantasma-comum.png"
    },

    {
        "id": 2,
        "nome": "Fantasma Incomum (Gravata)",
        "raridade": "Incomum",
        "chance": 25,
        "urlImagem": "/static/img/fantasma-incomum.png"
    },

    {
        "id": 3,
        "nome": "Fantasma Épico (Ceifador)",
        "raridade": "Épico",
        "chance": 15,
        "urlImagem": "/static/img/fantasma-epico.png"
    },

    {
        "id": 4,
        "nome": "Lorde Fantasma",
        "raridade": "Lendário",
        "chance": 10,
        "urlImagem": "/static/img/fantasma-lendario.png"
    }
]

ARQUIVO_JSON = "jogador.json"


# =========================
# CRIAR JSON SE NÃO EXISTIR
# =========================

def criar_arquivo():

    if not os.path.exists(ARQUIVO_JSON):

        dados_iniciais = {
            "colecao": []
        }

        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:

            json.dump(
                dados_iniciais,
                arquivo,
                indent=4,
                ensure_ascii=False
            )


# =========================
# LER COLEÇÃO
# =========================

def ler_colecao():

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:

        dados = json.load(arquivo)

    return dados


# =========================
# SALVAR COLEÇÃO
# =========================

def salvar_colecao(dados):

    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


# =========================
# SISTEMA DE SORTEIO
# =========================

def sortear_fantasma():

    numero_sorteado = random.uniform(0, 100)

    chance_acumulada = 0

    for fantasma in banco_de_fantasmas:

        chance_acumulada += fantasma["chance"]

        if numero_sorteado <= chance_acumulada:

            return fantasma

    return banco_de_fantasmas[0]


# =========================
# ROTA PRINCIPAL
# =========================

@app.route("/")
def home():

    return render_template("index.html")


# =========================
# CAPTURAR FANTASMA
# =========================

@app.route("/capturar")
def capturar():

    fantasma = sortear_fantasma()

    dados = ler_colecao()

    # EVITAR DUPLICADOS
    ja_existe = any(
        f["id"] == fantasma["id"]
        for f in dados["colecao"]
    )

    if not ja_existe:

        dados["colecao"].append(fantasma)

        salvar_colecao(dados)

    return jsonify({
        "fantasma": fantasma,
        "duplicado": ja_existe
    })


# =========================
# VER COLEÇÃO
# =========================

@app.route("/colecao")
def colecao():

    dados = ler_colecao()

    return jsonify(dados)


# =========================
# LIMPAR COLEÇÃO
# =========================

@app.route("/limpar")
def limpar():

    dados = {
        "colecao": []
    }

    salvar_colecao(dados)

    return jsonify({
        "mensagem": "Coleção limpa com sucesso"
    })


# =========================
# INICIAR SERVIDOR
# =========================

if __name__ == "__main__":

    criar_arquivo()

    app.run(debug=True)