from app.tools.rag_tool import buscar_material_rag
from app.llm.client import ask_llm

import json
from pathlib import Path

ACTIVE_RECALL_PATH = Path("app/memory/active_recall.json")


def carregar_dados():
    if ACTIVE_RECALL_PATH.exists():
        with open(ACTIVE_RECALL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "aguardando_resposta": False,
        "historico": []
    }


def salvar_dados(dados):
    ACTIVE_RECALL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ACTIVE_RECALL_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def gerar_pergunta_active_recall(termo_busca, **kwargs):
    contexto = buscar_material_rag(termo_busca)

    prompt = f"""
Com base no material abaixo, gere UMA pergunta de revisão para um estudante.

Não invente fontes, nomes de arquivos ou trechos que não estejam no contexto.
Se o contexto estiver fraco, gere uma pergunta simples e diretamente ligada ao tema.

Tema:
{termo_busca}

Material:
{contexto}

Gere apenas a pergunta.
"""

    pergunta = ask_llm(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    ).strip()

    dados = carregar_dados()

    dados["historico"].append({
        "pergunta": pergunta,
        "termo_busca": termo_busca,
        "respondida": False,
        "resposta_aluno": "",
        "avaliacao": ""
    })

    dados["aguardando_resposta"] = True
    salvar_dados(dados)

    return pergunta


def avaliar_resposta_active_recall(resposta_usuario, **kwargs):
    dados = carregar_dados()

    if not dados.get("aguardando_resposta", False):
        return "Não há pergunta de Active Recall aguardando resposta."

    pergunta_pendente = None
    for item in reversed(dados["historico"]):
        if not item["respondida"]:
            pergunta_pendente = item
            break

    if pergunta_pendente is None:
        dados["aguardando_resposta"] = False
        salvar_dados(dados)
        return "Nenhuma pergunta pendente para avaliação."

    pergunta = pergunta_pendente["pergunta"]
    termo_busca = pergunta_pendente["termo_busca"]

    # AQUI está a correção importante:
    # usa o tema original, não a pergunta gerada.
    contexto = buscar_material_rag(termo_busca)

    prompt = f"""
Você é um avaliador acadêmico.

Use somente o material fornecido abaixo.
Não invente fontes, documentos, arquivos ou trechos que não estejam no contexto.
Se o contexto for insuficiente, diga isso explicitamente.

Pergunta original do exercício:
{pergunta}

Tema:
{termo_busca}

Resposta do aluno:
{resposta_usuario}

Material de apoio:
{contexto}

Classifique a resposta em uma destas opções:
- Correta
- Parcialmente correta
- Incorreta

Depois explique brevemente o motivo.
"""

    avaliacao = ask_llm(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    ).strip()

    pergunta_pendente["respondida"] = True
    pergunta_pendente["resposta_aluno"] = resposta_usuario
    pergunta_pendente["avaliacao"] = avaliacao

    dados["aguardando_resposta"] = False
    salvar_dados(dados)

    return avaliacao