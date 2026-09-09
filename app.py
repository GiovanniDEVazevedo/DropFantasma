# =========================
# app.py
# FLASK WEB APP
# =========================

from flask import Flask, jsonify, render_template, request
from utils import criar_save, ler_save, salvar_save
import random
import copy

app = Flask(__name__)

BANCO_DE_FANTASMAS = [
    {
        "id": 1,
        "nome": "Fantasma Comum",
        "raridade": "Comum",
        "pontos": 20,
        "urlImagem": "/static/img/fantasma-comum.png"
    },
    {
        "id": 2,
        "nome": "Fantasma Incomum",
        "raridade": "Incomum",
        "pontos": 40,
        "urlImagem": "/static/img/fantasma-incomum.png"
    },
    {
        "id": 3,
        "nome": "Fantasma Raro",
        "raridade": "Raro",
        "pontos": 60,
        "urlImagem": "/static/img/fantasma-raro.png"
    },
    {
        "id": 4,
        "nome": "Fantasma Épico",
        "raridade": "Épico",
        "pontos": 80,
        "urlImagem": "/static/img/fantasma-epico.png"
    },
    {
        "id": 5,
        "nome": "Lorde Fantasma",
        "raridade": "Lendário",
        "pontos": 120,
        "urlImagem": "/static/img/fantasma-lendario.png"
    }
]

PESOS = [50, 25, 15, 7, 3]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/capturar", methods=["POST"])
def capturar():
    dados = ler_save()
    fantasma_sorteado = random.choices(
        BANCO_DE_FANTASMAS, weights=PESOS, k=1
    )[0]

    fantasma_na_colecao = next(
        (f for f in dados["colecao"] if f["id"] == fantasma_sorteado["id"]),
        None
    )

    if fantasma_na_colecao:
        fantasma_na_colecao["quantidade"] += 1
        ja_existe = True
    else:
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


@app.route("/colecao")
def colecao():
    dados = ler_save()
    return jsonify(dados)


@app.route("/trocar", methods=["POST"])
def trocar_repetidos():
    dados = ler_save()
    trocados = 0
    pontos_ganhos = 0

    for fantasma in dados["colecao"]:
        extras = fantasma.get("quantidade", 1) - 1
        if extras > 0:
            pontos_ganhos += extras * fantasma["pontos"]
            trocados += extras
            fantasma["quantidade"] = 1

    dados["pontos"] += pontos_ganhos
    salvar_save(dados)

    return jsonify({
        "trocados": trocados,
        "pontos_ganhos": pontos_ganhos,
        "pontos": dados["pontos"]
    })


if __name__ == "__main__":
    criar_save()
    debug = True
    app.run(host="127.0.0.1", port=5000, debug=debug)
