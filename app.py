<<<<<<< HEAD
from flask import Flask, jsonify, render_template
=======
# =========================
# app.py
# FLASK WEB APP
# =========================

from flask import (
    Flask,
    jsonify,
    render_template
)

>>>>>>> desenvolvimento
import random
import json
import os

app = Flask(__name__)

<<<<<<< HEAD
=======
ARQUIVO_JSON = "jogador.json"


>>>>>>> desenvolvimento
# =========================
# BANCO DE FANTASMAS
# =========================

banco_de_fantasmas = [
<<<<<<< HEAD
=======

>>>>>>> desenvolvimento
    {
        "id": 1,
        "nome": "Fantasma Comum",
        "raridade": "Comum",
<<<<<<< HEAD
        "chance": 50,
        "urlImagem": "/static/img/fantasma-comum.png"
=======
        "pontos": 20,
        "urlImagem":
        "/static/img/fantasma-comum.png"
>>>>>>> desenvolvimento
    },

    {
        "id": 2,
<<<<<<< HEAD
        "nome": "Fantasma Incomum (Gravata)",
        "raridade": "Incomum",
        "chance": 25,
        "urlImagem": "/static/img/fantasma-incomum.png"
=======
        "nome": "Fantasma Incomum",
        "raridade": "Incomum",
        "pontos": 40,
        "urlImagem":
        "/static/img/fantasma-incomum.png"
>>>>>>> desenvolvimento
    },

    {
        "id": 3,
<<<<<<< HEAD
        "nome": "Fantasma Épico (Ceifador)",
        "raridade": "Épico",
        "chance": 15,
        "urlImagem": "/static/img/fantasma-epico.png"
=======
        "nome": "Fantasma Épico",
        "raridade": "Épico",
        "pontos": 80,
        "urlImagem":
        "/static/img/fantasma-epico.png"
>>>>>>> desenvolvimento
    },

    {
        "id": 4,
        "nome": "Lorde Fantasma",
        "raridade": "Lendário",
<<<<<<< HEAD
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
=======
        "pontos": 120,
        "urlImagem":
        "/static/img/fantasma-lendario.png"
    }
]


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
>>>>>>> desenvolvimento
                arquivo,
                indent=4,
                ensure_ascii=False
            )


# =========================
<<<<<<< HEAD
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
=======
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
# SALVAR SAVE
# =========================

def salvar_save(dados):

    with open(
        ARQUIVO_JSON,
        "w",
        encoding="utf-8"
    ) as arquivo:
>>>>>>> desenvolvimento

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


# =========================
<<<<<<< HEAD
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
=======
# HOME
>>>>>>> desenvolvimento
# =========================

@app.route("/")
def home():

    return render_template("index.html")


# =========================
<<<<<<< HEAD
# CAPTURAR FANTASMA
=======
# CAPTURAR
>>>>>>> desenvolvimento
# =========================

@app.route("/capturar")
def capturar():

<<<<<<< HEAD
    fantasma = sortear_fantasma()

    dados = ler_colecao()

    # EVITAR DUPLICADOS
    ja_existe = any(
        f["id"] == fantasma["id"]
=======
    dados = ler_save()

    fantasma = random.choice(
        banco_de_fantasmas
    )

    ja_existe = any(

        f["id"] == fantasma["id"]

>>>>>>> desenvolvimento
        for f in dados["colecao"]
    )

    if not ja_existe:

        dados["colecao"].append(fantasma)

<<<<<<< HEAD
        salvar_colecao(dados)

    return jsonify({
        "fantasma": fantasma,
        "duplicado": ja_existe
=======
        dados["pontos"] += fantasma["pontos"]

        salvar_save(dados)

    return jsonify({

        "fantasma": fantasma,

        "duplicado": ja_existe,

        "pontos": dados["pontos"]
>>>>>>> desenvolvimento
    })


# =========================
<<<<<<< HEAD
# VER COLEÇÃO
=======
# COLEÇÃO
>>>>>>> desenvolvimento
# =========================

@app.route("/colecao")
def colecao():

<<<<<<< HEAD
    dados = ler_colecao()
=======
    dados = ler_save()
>>>>>>> desenvolvimento

    return jsonify(dados)


# =========================
<<<<<<< HEAD
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
=======
# START
>>>>>>> desenvolvimento
# =========================

if __name__ == "__main__":

<<<<<<< HEAD
    criar_arquivo()

    app.run(debug=True)
=======
    criar_save()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
>>>>>>> desenvolvimento
