from app.rag.retrieval import retrieve_relevant_chunks


def buscar_material_rag(termo_busca: str) -> str:
    if not termo_busca or not termo_busca.strip():
        return "Erro: O termo de busca não pode estar vazio."
        
    chunks = retrieve_relevant_chunks(termo_busca, top_k=2)
    
    if not chunks:
        return "Nenhum material acadêmico relevante encontrado sobre esse assunto."
        
    contexto = "Resultados encontrados nos materiais de estudo:\n\n"
    for item in chunks:
        contexto += f"--- [Fonte: {item['filename']}] ---\n"
        contexto += f"{item['chunk']}\n\n"
        
    return contexto