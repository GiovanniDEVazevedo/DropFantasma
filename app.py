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
import copy

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
        "/static/img/fantasma-comum.png",
        "quantidade": 0

    },

    {
        "id": 2,
        "nome": "Fantasma Incomum",
        "raridade": "Incomum",
        "pontos": 40,
        "urlImagem":
        "/static/img/fantasma-incomum.png",
        "quantidade":0
    },

    {
        "id": 3,
        "nome": "Fantasma Épico",
        "raridade": "Épico",
        "pontos": 80,
        "urlImagem":
        "/static/img/fantasma-epico.png",
        "quantidade":0
    },

    {
        "id": 4,
        "nome": "Lorde Fantasma",
        "raridade": "Lendário",
        "pontos": 120,
        "urlImagem":
        "/static/img/fantasma-lendario.png",
        "quantidade":0
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

    # 1. Definindo as chances (ex: 60% Comum, 25% Incomum, 10% Épico, 5% Lendário)
    pesos = [60, 25, 10, 5]
    
    # random.choices retorna uma lista, pegamos o índice [0]
    fantasma_sorteado = random.choices(banco_de_fantasmas, weights=pesos, k=1)[0]
    
    # 2. Verifica se já existe na coleção
    fantasma_na_colecao = next((f for f in dados["colecao"] if f["id"] == fantasma_sorteado["id"]), None)

    if fantasma_na_colecao:
        # Se já existe, apenas incrementamos a quantidade
        fantasma_na_colecao["quantidade"] += 1
        ja_existe = True
    else:
        # Se não existe, criamos uma cópia para não alterar o banco original
        novo_fantasma = copy.deepcopy(fantasma_sorteado)
        novo_fantasma["quantidade"] = 1
        dados["colecao"].append(novo_fantasma)
        dados["pontos"] += novo_fantasma["pontos"]
        ja_existe = False

    salvar_save(dados)

    return jsonify({
        "fantasma": fantasma_sorteado,
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