import json
import os
import traceback
from datetime import datetime
from app.tools.agenda import consultar_agenda
from app.tools.tarefas import adicionar_tarefa, listar_tarefas, concluir_tarefa
from app.tools.rag_tool import buscar_material_rag
from app.tools.planejamento_estudos import planejar_estudos
from app.tools.active_recall import (
    gerar_pergunta_active_recall,
    avaliar_resposta_active_recall
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, "logs", "tool_logs.json")

FERRAMENTAS_CONFIG = [
    {
        "type": "function",
        "function": {
            "name": "consultar_agenda",
            "description": "Consulta compromissos acadêmicos. Pode filtrar por data ou por tipo (AULA, PROVA, ENTREGA, PALESTRA).",
            "parameters": {
                "type": "object",
                "properties": {
                    "data_pesquisa": {
                        "type": "string",
                        "description": "Data no formato AAAA-MM-DD."
                    },
                    "tipo": {
                        "type": "string",
                        "description": "AULA, PROVA, ENTREGA ou PALESTRA."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_tarefas",
            "description": "Lista tarefas. Pode filtrar por status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filtro opcional: Pendente ou Concluída."
                    }
                }
            }
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
    },
    {
        "type": "function",
        "function": {
            "name": "planejar_estudos",
            "description": "Cria um plano de estudos, sugere prioridades ou orienta a organização dos estudos do aluno.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pergunta_usuario": {
                        "type": "string",
                        "description": "Pergunta original do aluno."
                    }
                },
                "required": ["pergunta_usuario"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gerar_pergunta_active_recall",
            "description": "Gera uma pergunta de revisão.",
            "parameters": {
                "type": "object",
                "properties": {
                    "termo_busca": {
                        "type": "string",
                        "description": "Tema da pergunta."
                    }
                },
                "required": ["termo_busca"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "avaliar_resposta_active_recall",
            "description": "Avalia a resposta de uma pergunta de active recall que foi feita anteriormente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "resposta_usuario": {
                        "type": "string",
                        "description": "Resposta fornecida pelo aluno."
                    }
                },
                "required": ["resposta_usuario"]
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
        "buscar_material_rag": buscar_material_rag,
        "planejar_estudos": planejar_estudos,
        "gerar_pergunta_active_recall": gerar_pergunta_active_recall,
        "avaliar_resposta_active_recall": avaliar_resposta_active_recall
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