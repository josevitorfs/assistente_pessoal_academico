import sys
import os
from dotenv import load_dotenv
import json
from app.llm.client import ask_llm
from app.tools.orquestrador import executar_ferramenta
from pathlib import Path

ACTIVE_RECALL_PATH = Path("app/memory/active_recall.json")

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def existe_pergunta_active_recall_pendente():
    if not ACTIVE_RECALL_PATH.exists():
        return False

    with open(ACTIVE_RECALL_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)

    return dados.get("aguardando_resposta", False)

def executar_fluxo_jarvis(pergunta_usuario: str) -> str:
    if existe_pergunta_active_recall_pendente():
        print("\nJARVIS: Executando rota 'avaliar_resposta_active_recall'...")

        return executar_ferramenta(
            "avaliar_resposta_active_recall",
            {
                "resposta_usuario": pergunta_usuario
            }
        )
            
    prompt_analise = (
        "Você é o motor de rotas do JARVIS.\n"
        "Hoje é terça, 26 de maio de 2026.\n\n"
        "Sua única saída permitida é um objeto JSON com as chaves:\n"
        "- 'acao': string contendo 'listar_tarefas', 'adicionar_tarefa', 'concluir_tarefa', 'consultar_agenda', 'buscar_material_rag', 'planejar_estudos' ou 'conversar'.\n"
        "Use 'listar_tarefas' para:\n"
        "- listar tarefas\n"
        "- mostrar atividades\n"
        "- mostrar tarefas\n\n"

        "Se o usuário pedir APENAS tarefas pendentes, use:\n"

        "{\n"
        '  "acao": "listar_tarefas",\n'
        '  "params": {\n'
        '    "status": "Pendente"\n'
        '  }\n'
        "}\n\n"

        "Se o usuário pedir APENAS tarefas concluídas, use:\n"

        "{\n"
        '  "acao": "listar_tarefas",\n'
        '  "params": {\n'
        '    "status": "Concluída"\n'
        '  }\n'
        "}\n\n"

        "Se ele pedir todas as tarefas, use:\n"

        "{\n"
        '  "acao": "listar_tarefas",\n'
        '  "params": {}\n'
        "}\n\n"
        "Use 'planejar_estudos' quando o usuário pedir:"
        "- plano de estudos"
        "- planejamento"
        "- organização dos estudos"
        "- prioridades"
        "- o que devo estudar"
        "- o que devo priorizar hoje"
        "- qual tarefa devo fazer agora"
        "- no que devo focar"
        "- o que é mais importante"
        "- como organizar minha semana"
        "- como organizar meus estudos\n"
        "Use 'gerar_pergunta_active_recall' quando o usuário pedir uma pergunta de revisão, teste de conhecimento, quiz, active recall ou disser algo como 'me faça uma pergunta sobre embeddings'.\n"
        "Use 'avaliar_resposta_active_recall' quando existir uma pergunta pendente e o usuário estiver respondendo essa pergunta.\n"
        "{\"acao\": \"planejar_estudos\", "
        "\"params\": {\"pergunta_usuario\": \"<pergunta original>\"}}\n\n"
        "- 'params': objeto com os argumentos da função.\n\n"
        "Regra para buscar_material_rag: Use SEMPRE que o usuário fizer perguntas conceituais, dúvidas de matérias, pedir explicações ou resumos (ex: {'termo_busca': 'regressão linear'}).\n\n"
        "Exemplo de saída para listagem:\n"
        "Sempre que a ação for adicionar_tarefa, use as chaves titulo e data_prazo.\n"
        "{\"acao\": \"listar_tarefas\", \"params\": {}}\n\n"
        f"Pedido do usuário: {pergunta_usuario}\n"
        "Resposta JSON:"
    )

    try:
        conteudo = ask_llm(messages=[
                            {
                                "role": "user",
                                "content": prompt_analise
                            }
                        ],
                        temperature=0.1
                            ).strip()
        
        if "```" in conteudo:
            conteudo = conteudo.split("```")[1]
            if conteudo.startswith("json"):
                conteudo = conteudo[4:]
        conteudo = conteudo.strip()

        dados_intencao = json.loads(conteudo)
        acao = dados_intencao.get("acao", "conversar")
        params = dados_intencao.get("params", {})

        if acao == "conversar":
            return ask_llm(
                            messages=[
                                {
                                    "role": "user",
                                    "content": pergunta_usuario
                                }
                            ]
                        )

        print(f"\nJARVIS: Executando rota '{acao}'...")
        resultado_local = executar_ferramenta(acao, params)

        if acao in [
            "listar_tarefas",
            "consultar_agenda",
            "gerar_pergunta_active_recall",
            "avaliar_resposta_active_recall",
            "planejar_estudos"
        ]:
            return resultado_local

        if acao == "buscar_material_rag":
            prompt_resposta = (
                f"O estudante perguntou: '{pergunta_usuario}'\n\n"
                f"Responda de forma didática baseando-se estritamente nestes trechos do material dele:\n"
                f"{resultado_local}"
            )
            return ask_llm(
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt_resposta
                                }
                            ],
                            temperature=0.4
                        )

        return ask_llm(
                        messages=[
                            {
                                "role": "system",
                                "content": "Confirme o sucesso da operação de forma breve e amigável com base no resultado enviado."
                            },
                            {
                                "role": "user",
                                "content": f"Resultado: {resultado_local}"
                            }
                        ],
                        temperature=0.5
                    )

    except Exception as e:
        return f"Erro na orquestração central do Jarvis: {str(e)}"


def main():
    print("                                                      JARVIS ACADÊMICO - SISTEMA ESTÁVEL                                        ")
    while True:
        try:
            pergunta = input("\nVocê: ")
            if pergunta.strip().lower() in ["sair", "exit", "quit"]:
                break
            if not pergunta.strip():
                continue
            
            resposta_final = executar_fluxo_jarvis(pergunta)
            print(f"\nJARVIS:\n{resposta_final}")
            print("\n" + "_"*60)
        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == "__main__":
    main()