import numpy as np
from app.rag.vectordb import load_db
from app.rag.embeddings import generate_query_embedding


def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2) if norm_v1 and norm_v2 else 0.0

def retrieve_relevant_chunks(query: str, top_k: int = 3) -> list:
    db = load_db()
    if not db:
        return []
        
    query_emb = generate_query_embedding(query)
    scored_chunks = []
    
    for item in db:
        score = cosine_similarity(query_emb, item["embedding"])
        scored_chunks.append((score, item))
        
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    return [
        {
            **item,
            "score": float(score)
        }
        for score, item in scored_chunks[:top_k]
        ]