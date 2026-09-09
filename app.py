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
        "chance": 75,
        "urlImagem": "/static/img/fantasma-comum.png"
    },
    {
        "id": 2,
        "nome": "Fantasma Incomum",
        "raridade": "Incomum",
        "pontos": 40,
        "chance": 65,
        "urlImagem": "/static/img/fantasma-incomum.png"
    },
    {
        "id": 3,
        "nome": "Fantasma Raro",
        "raridade": "Raro",
        "pontos": 60,
        "chance": 50,
        "urlImagem": "/static/img/fantasma-raro.png"
    },
    {
        "id": 4,
        "nome": "Fantasma Épico",
        "raridade": "Épico",
        "pontos": 80,
        "chance": 35,
        "urlImagem": "/static/img/fantasma-epico.png"
    },
    {
        "id": 5,
        "nome": "Lorde Fantasma",
        "raridade": "Lendário",
        "pontos": 120,
        "chance": 20,
        "urlImagem": "/static/img/fantasma-lendario.png"
    }
]

PESOS = [50, 25, 15, 7, 3]
PESOS_INCENSO = [5, 15, 20, 30, 30]
CHANCE_MAXIMA = 95

MERCADO = [
    {
        "id": "frasco",
        "nome": "Frasco de Sorte",
        "preco": 50,
        "descricao": "+25% de chance de captura em 1 tentativa"
    },
    {
        "id": "cristal",
        "nome": "Cristal de Captura",
        "preco": 100,
        "descricao": "Garante a captura do proximo fantasma"
    },
    {
        "id": "incenso",
        "nome": "Incenso de Raridade",
        "preco": 80,
        "descricao": "Aumenta a chance de Epico e Lendario em 1 tentativa"
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/capturar", methods=["POST"])
def capturar():
    dados = ler_save()
    itens = dados["itens"]

    usar_incenso = itens["incenso"] > 0
    pesos_atual = PESOS_INCENSO if usar_incenso else PESOS
    if usar_incenso:
        itens["incenso"] -= 1

    fantasma_sorteado = random.choices(
        BANCO_DE_FANTASMAS, weights=pesos_atual, k=1
    )[0]

    usar_cristal = itens["cristal"] > 0
    if usar_cristal:
        itens["cristal"] -= 1
        sucesso = True
    else:
        usar_frasco = itens["frasco"] > 0
        chance = fantasma_sorteado["chance"] + 25 if usar_frasco else fantasma_sorteado["chance"]
        if usar_frasco:
            itens["frasco"] -= 1
        chance = min(CHANCE_MAXIMA, chance)
        sucesso = random.randint(1, 100) <= chance

    if not sucesso:
        salvar_save(dados)
        return jsonify({
            "capturado": False,
            "fantasma": fantasma_sorteado,
            "pontos": dados["pontos"],
            "itens": itens
        })

    fantasma_na_colecao = next(
        (f for f in dados["colecao"] if f["id"] == fantasma_sorteado["id"]),
        None
    )

    if fantasma_na_colecao:
        fantasma_na_colecao["quantidade"] += 1
        ja_existe = True
        pontos_ganhos = 0
    else:
        novo_fantasma = copy.deepcopy(fantasma_sorteado)
        novo_fantasma["quantidade"] = 1
        dados["colecao"].append(novo_fantasma)
        dados["pontos"] += novo_fantasma["pontos"]
        ja_existe = False
        pontos_ganhos = novo_fantasma["pontos"]

    salvar_save(dados)

    return jsonify({
        "capturado": True,
        "fantasma": fantasma_sorteado,
        "duplicado": ja_existe,
        "pontos_ganhos": pontos_ganhos,
        "pontos": dados["pontos"],
        "itens": itens
    })


@app.route("/colecao")
def colecao():
    dados = ler_save()
    return jsonify(dados)


@app.route("/mercado")
def mercado():
    dados = ler_save()
    return jsonify({
        "itens": MERCADO,
        "inventario": dados["itens"],
        "pontos": dados["pontos"]
    })


@app.route("/comprar", methods=["POST"])
def comprar():
    dados = ler_save()
    corpo = request.get_json(silent=True) or {}
    item_id = corpo.get("item", "")

    item = next((i for i in MERCADO if i["id"] == item_id), None)
    if item is None:
        return jsonify({"erro": "Item invalido"}), 400

    if dados["pontos"] < item["preco"]:
        return jsonify({
            "erro": "Pontos insuficientes",
            "pontos": dados["pontos"]
        }), 400

    dados["pontos"] -= item["preco"]
    dados["itens"][item_id] += 1
    salvar_save(dados)

    return jsonify({
        "sucesso": True,
        "item": item["nome"],
        "preco": item["preco"],
        "pontos": dados["pontos"],
        "inventario": dados["itens"]
    })


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