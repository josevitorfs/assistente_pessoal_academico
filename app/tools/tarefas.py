import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAREFAS_PATH = os.path.join(BASE_DIR, "memory", "tarefas.json")

def adicionar_tarefa(titulo: str, data_prazo: str = "undefined") -> str:
    tarefas = []
    if os.path.exists(TAREFAS_PATH):
        try:
            with open(TAREFAS_PATH, "r", encoding="utf-8") as f:
                tarefas = json.load(f)
        except Exception:
            tarefas = []

    novo_id = max([t.get("id", 0) for t in tarefas], default=0) + 1

    nova_tarefa = {
        "id": novo_id,
        "titulo": titulo.strip(),
        "status": "Pendente",
        "data_prazo": data_prazo.strip()
    }

    tarefas.append(nova_tarefa)
    os.makedirs(os.path.dirname(TAREFAS_PATH), exist_ok=True)
    
    with open(TAREFAS_PATH, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=2, ensure_ascii=False)

    prazo_str = f" com prazo para {data_prazo}" if data_prazo != "undefined" else ""
    return f"Tarefa '[{novo_id}] {titulo}' adicionada com sucesso{prazo_str}."


def listar_tarefas() -> str:
    if not os.path.exists(TAREFAS_PATH):
        return "Sua Lista de Tarefas está vazia."

    try:
        with open(TAREFAS_PATH, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                return "Sua Lista de Tarefas está vazia."
            tarefas = json.loads(conteudo)
    except Exception as e:
        return f"Erro interno ao decodificar o JSON: {str(e)}"

    if not tarefas:
        return "Sua Lista de Tarefas está vazia."

    resultado = "Sua Lista de Tarefas:\n"
    for t in tarefas:
        prazo = f" (Prazo: {t['data_prazo']})" if t.get("data_prazo") != "undefined" else ""
        resultado += f"- [{t['id']}] {t['titulo']}{prazo} - {t['status']}\n"
    
    return resultado

def concluir_tarefa(id_tarefa: int = None, titulo: str = None, busca_contextual: str = None) -> str:
    if not os.path.exists(TAREFAS_PATH):
        return "Sua Lista de Tarefas está vazia."

    try:
        with open(TAREFAS_PATH, "r", encoding="utf-8") as f:
            tarefas = json.load(f)
    except Exception:
        return "Erro ao ler o arquivo de tarefas."

    tarefa_encontrada = None

    if id_tarefa is not None:
        try:
            id_busca = int(id_tarefa)
            for t in tarefas:
                if t.get("id") == id_busca:
                    tarefa_encontrada = t
                    break
        except ValueError:
            pass

    if not tarefa_encontrada and titulo:
        busca_lower = titulo.lower().strip()
        for t in tarefas:
            if busca_lower in t.get("titulo", "").lower():
                tarefa_encontrada = t
                break

    if not tarefa_encontrada and busca_contextual:
        busca_lower = busca_contextual.lower().strip()
        for t in tarefas:
            if busca_lower in t.get("titulo", "").lower() or busca_lower in t.get("data_prazo", "").lower():
                tarefa_encontrada = t
                break

    if not tarefa_encontrada:
        return "Nenhuma tarefa correspondente foi encontrada para ser concluída."

    tarefa_encontrada["status"] = "Concluída"

    with open(TAREFAS_PATH, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=2, ensure_ascii=False)

    return f"Tarefa '{tarefa_encontrada['titulo']}' [ID {tarefa_encontrada['id']}] marcada como concluída com sucesso!"