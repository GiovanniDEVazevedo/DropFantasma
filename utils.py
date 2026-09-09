import json
import os

DIRETORIO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(DIRETORIO, "jogador.json")


def criar_save():
    if not os.path.exists(ARQUIVO_JSON):
        dados = {"colecao": [], "pontos": 0}
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def ler_save():
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        criar_save()
        return {"colecao": [], "pontos": 0}


def salvar_save(dados):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
