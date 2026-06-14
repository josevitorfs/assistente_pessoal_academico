from app.rag.retrieval import retrieve_relevant_chunks


def buscar_material_rag(termo_busca: str) -> str:
    if not termo_busca or not termo_busca.strip():
        return "Erro: O termo de busca não pode estar vazio."

    chunks = retrieve_relevant_chunks(termo_busca, top_k=3)

    if not chunks:
        return "Nenhum material acadêmico relevante encontrado sobre esse assunto."

    contexto = "Resultados encontrados nos materiais de estudo:\n\n"

    for item in chunks:
        contexto += (
            f"--- [Fonte: {item['filename']}] "
            f"(score={item['score']:.4f}) ---\n"
        )
        contexto += f"{item['chunk']}\n\n"

    return contexto

def obter_fontes_recuperadas(termo_busca: str):
    chunks = retrieve_relevant_chunks(termo_busca, top_k=3)

    return [
        {
            "arquivo": item["filename"],
            "score": round(item["score"], 4)
        }
        for item in chunks
    ]