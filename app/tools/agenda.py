import json
import os

AGENDA_PATH = "app/memory/agenda.json"

def consultar_agenda(data_pesquisa=None, data=None, tipo=None, **kwargs):

    if data and not data_pesquisa:
        data_pesquisa = data

    if not os.path.exists(AGENDA_PATH):
        return "A agenda está vazia ou o arquivo não foi encontrado."

    try:
        with open(AGENDA_PATH, "r", encoding="utf-8") as f:
            compromissos = json.load(f)
    except Exception as e:
        return f"Erro ao ler o arquivo de agenda: {str(e)}"

    if tipo:
        compromissos = [
            c for c in compromissos
            if c["tipo"].upper() == tipo.upper()
        ]

    if data_pesquisa:
        compromissos = [
            c for c in compromissos
            if c["data"] == data_pesquisa
        ]

    if not compromissos:
        return "Nenhum compromisso encontrado."

    resultado = "Compromissos encontrados:\n"

    for c in compromissos:
        resultado += f"- {c['data']}: [{c['tipo'].upper()}] {c['descricao']}\n"

    return resultado