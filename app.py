# =========================
# app.py
# FLASK WEB APP
# =========================

from flask import (
    Flask,
    jsonify,
    render_template
)

import random
import json
import os

app = Flask(__name__)

ARQUIVO_JSON = "jogador.json"


# =========================
# BANCO DE FANTASMAS
# =========================

banco_de_fantasmas = [

    {
        "id": 1,
        "nome": "Fantasma Comum",
        "raridade": "Comum",
        "pontos": 20,
        "urlImagem":
        "/static/img/fantasma-comum.png"
    },

    {
        "id": 2,
        "nome": "Fantasma Incomum",
        "raridade": "Incomum",
        "pontos": 40,
        "urlImagem":
        "/static/img/fantasma-incomum.png"
    },

    {
        "id": 3,
        "nome": "Fantasma Épico",
        "raridade": "Épico",
        "pontos": 80,
        "urlImagem":
        "/static/img/fantasma-epico.png"
    },

    {
        "id": 4,
        "nome": "Lorde Fantasma",
        "raridade": "Lendário",
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
# SALVAR SAVE
# =========================

def salvar_save(dados):

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
# HOME
# =========================

@app.route("/")
def home():

    return render_template("index.html")


# =========================
# CAPTURAR
# =========================

@app.route("/capturar")
def capturar():

    dados = ler_save()

    fantasma = random.choice(
        banco_de_fantasmas
    )

    ja_existe = any(

        f["id"] == fantasma["id"]

        for f in dados["colecao"]
    )

    if not ja_existe:

        dados["colecao"].append(fantasma)

        dados["pontos"] += fantasma["pontos"]

        salvar_save(dados)

    return jsonify({

        "fantasma": fantasma,

        "duplicado": ja_existe,

        "pontos": dados["pontos"]
    })


# =========================
# COLEÇÃO
# =========================

@app.route("/colecao")
def colecao():

    dados = ler_save()

    return jsonify(dados)


# =========================
# START
# =========================

if __name__ == "__main__":

    criar_save()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )