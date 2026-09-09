import json
import os

DIRETORIO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(DIRETORIO, "jogador.json")

ITENS_INICIAIS = {
    "frasco": 0,
    "cristal": 0,
    "incenso": 0
}


def criar_save():
    if not os.path.exists(ARQUIVO_JSON):
        dados = {
            "colecao": [],
            "pontos": 0,
            "itens": dict(ITENS_INICIAIS)
        }
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def ler_save():
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        criar_save()
        dados = {"colecao": [], "pontos": 0, "itens": dict(ITENS_INICIAIS)}
        return dados

    if "itens" not in dados:
        dados["itens"] = dict(ITENS_INICIAIS)

    for chave in ITENS_INICIAIS:
        dados["itens"].setdefault(chave, 0)

    return dados


def salvar_save(dados):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)