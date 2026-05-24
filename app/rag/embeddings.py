from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embeddings(texts: list) -> list:
    return model.encode(texts, convert_to_numpy=True).tolist()

def generate_query_embedding(query: str) -> list:

    return model.encode(query, convert_to_numpy=True).tolist()