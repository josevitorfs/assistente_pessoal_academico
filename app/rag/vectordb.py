import pickle
import os

DB_PATH = "app/memory/vector_store.pkl"

def save_to_db(chunks: list, embeddings: list, filenames: list):
    data = []
    for chunk, emb, fname in zip(chunks, embeddings, filenames):
        data.append({
            "chunk": chunk,
            "embedding": emb,
            "filename": fname
        })
        
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "wb") as f:
        pickle.dump(data, f)

def load_db() -> list:
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "rb") as f:
        return pickle.load(f)