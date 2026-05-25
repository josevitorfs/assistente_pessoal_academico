from app.rag import retrieval


def test_retrieve_relevant_chunks_returns_top_match(monkeypatch):
    fake_db = [
        {"chunk": "conceito de regressao logistica", "embedding": [1.0, 0.0], "filename": "a.pdf"},
        {"chunk": "conceito de redes neurais", "embedding": [0.0, 1.0], "filename": "b.pdf"},
    ]

    monkeypatch.setattr(retrieval, "load_db", lambda: fake_db)
    monkeypatch.setattr(retrieval, "generate_query_embedding", lambda query: [1.0, 0.0])

    result = retrieval.retrieve_relevant_chunks("regressao logistica", top_k=1)

    assert len(result) == 1
    assert result[0]["filename"] == "a.pdf"