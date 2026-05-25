import json
import os
import traceback
from datetime import datetime
from app.tools.agenda import consultar_agenda
from app.tools.tarefas import adicionar_tarefa, listar_tarefas, concluir_tarefa
from app.tools.rag_tool import buscar_material_rag


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, "logs", "tool_logs.json")

FERRAMENTAS_CONFIG = [
    {
        "type": "function",
        "function": {
            "name": "consultar_agenda",
            "description": "Consulta os compromissos acadêmicos (aulas, provas, entregas) do estudante. Pode filtrar por uma data específica se fornecida.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data_pesquisa": {
                        "type": "string",
                        "description": "Data opcional no formato 'AAAA-MM-DD' (Ex: 2026-05-24)."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_tarefas",
            "description": "Lista todas as tarefas acadêmicas pendentes e concluídas do estudante com seus respectivos IDs.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "adicionar_tarefa",
            "description": "Adiciona uma nova tarefa acadêmica à lista. Se o usuário mencionar uma data relativa (como 'amanhã' ou 'quinta que vem') ou absoluta, calcule a data exata com base em hoje (23 de maio de 2026) e envie no formato 'AAAA-MM-DD'. Caso nenhuma data seja informada ou deduzida, use 'undefined'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "description": "O nome ou descrição da tarefa (Ex: 'Entrega de trabalho de IA')."},
                    "data_prazo": {"type": "string", "description": "Data calculada do prazo no formato 'AAAA-MM-DD', ou 'undefined' se não houver."}
                },
                "required": ["titulo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "concluir_tarefa",
            "description": "Marca uma tarefa específica como concluída usando o ID numérico dela.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_tarefa": {"type": "integer", "description": "O ID numérico da tarefa obtido na listagem."}
                },
                "required": ["id_tarefa"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_material_rag",
            "description": "Pesquisa nos materiais didáticos (PDFs) para responder a dúvidas conceituais e gerar explicações ou resumos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "termo_busca": {"type": "string", "description": "O assunto ou pergunta conceitual (Ex: 'regressão logística')."}
                },
                "required": ["termo_busca"]
            }
        }
    }
]

def registrar_log_ferramenta(nome_ferramenta: str, argumentos: dict, resultado: str):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ferramenta": nome_ferramenta,
        "entrada": argumentos,
        "saida": resultado
    }
    
    logs = []
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
            
    logs.append(log_entry)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)

def executar_ferramenta(nome_ferramenta: str, argumentos: dict) -> str:
    mapa_funcoes = {
        "consultar_agenda": consultar_agenda,
        "listar_tarefas": listar_tarefas,
        "adicionar_tarefa": adicionar_tarefa,
        "concluir_tarefa": concluir_tarefa,
        "buscar_material_rag": buscar_material_rag
    }
    
    if nome_ferramenta not in mapa_funcoes:
        return f"Erro: Ferramenta '{nome_ferramenta}' não implementada."
        
    try:
        if argumentos is None:
            argumentos = {}
            
        resultado = mapa_funcoes[nome_ferramenta](**argumentos)
    except Exception as e:
        print(f"\n❌ [ERRO CRÍTICO EM {nome_ferramenta}]: {str(e)}")
        traceback.print_exc()
        resultado = f"Erro na execução da ferramenta: {str(e)}"
        
    registrar_log_ferramenta(nome_ferramenta, argumentos, resultado)
    return resultado