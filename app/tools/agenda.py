import json
import os


AGENDA_PATH = "app/memory/agenda.json"

def consultar_agenda(data_pesquisa: str = None) -> str:
    if not os.path.exists(AGENDA_PATH):
        return "A agenda está vazia ou o arquivo não foi encontrado."

    try:
        with open(AGENDA_PATH, "r", encoding="utf-8") as f:
            compromissos = json.load(f)
    except Exception as e:
        return f"Erro ao ler o arquivo de agenda: {str(e)}"

    if data_pesquisa:
        filtrados = [c for c in compromissos if c["data"] == data_pesquisa]
        if not filtrados:
            return f"Nenhum compromisso agendado para o dia {data_pesquisa}."
        
        resultado = f"Compromissos para {data_pesquisa}:\n"
        for c in filtrados:
            resultado += f"- [{c['tipo'].upper()}] {c['descricao']}\n"
        return resultado

    else:
        if not compromissos:
            return "Nenhum compromisso na agenda."
        
        resultado = "Próximos compromissos na agenda:\n"
        for c in compromissos:
            resultado += f"- {c['data']}: [{c['tipo'].upper()}] {c['descricao']}\n"
        return resultado