from app.tools.agenda import consultar_agenda
from app.tools.tarefas import listar_tarefas
from app.llm.client import ask_llm


def planejar_estudos(pergunta_usuario, **kwargs):

    texto = pergunta_usuario.lower()

    if any(x in texto for x in [
        "priorizar",
        "prioridade",
        "focar",
        "urgente",
        "mais importante",
        "devo fazer agora",
        "estudar primeiro",
        "o que estudar hoje",
        "o que devo estudar hoje"
    ]):
        modo = "prioridades"

    elif any(x in texto for x in [
        "organizar",
        "organização",
        "organizacao",
        "dividir tempo",
        "rotina",
        "como estudar",
        "como organizar"
    ]):
        modo = "organizacao"

    else:
        modo = "cronograma"

    agenda = consultar_agenda()

    if modo == "prioridades":
        tarefas = listar_tarefas(status="Pendente")
    else:
        tarefas = listar_tarefas()

    prompt = f"""
Você é um orientador acadêmico especializado.

Modo atual:
{modo}

Pedido do aluno:
{pergunta_usuario}

Agenda do aluno:
{agenda}

Tarefas do aluno:
{tarefas}

REGRAS IMPORTANTES:

- Use SOMENTE informações presentes na agenda e nas tarefas.
- Não invente provas, trabalhos ou compromissos.
- Não escreva mensagens genéricas.
- Cite explicitamente os nomes das tarefas e eventos encontrados.
- Seja objetivo e prático.

SE MODO = prioridades:

1. Liste as 3 prioridades mais importantes.
2. Explique rapidamente por que cada uma é prioridade.
3. Considere nesta ordem:
   - provas;
   - entregas;
   - tarefas pendentes.

Formato:

1. Nome da atividade
   Motivo: ...

2. Nome da atividade
   Motivo: ...

SE MODO = organizacao:

Monte uma sequência prática dizendo:

- O que fazer primeiro.
- O que fazer depois.
- O que deixar por último.
- Quanto tempo dedicar para cada etapa.

SE MODO = cronograma:

Monte um cronograma semanal organizado.

Para cada atividade informe:

- atividade;
- prioridade;
- sugestão de período.

Se não houver tarefas suficientes, diga isso explicitamente.

Responda apenas com o planejamento.
"""

    return ask_llm(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )