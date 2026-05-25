from app.rag import vectordb


def test_save_and_load_db(tmp_path, monkeypatch):
    db_path = tmp_path / "vector_store.pkl"
    monkeypatch.setattr(vectordb, "DB_PATH", db_path)

    chunks = ["chunk 1", "chunk 2"]
    embeddings = [[1.0, 0.0], [0.0, 1.0]]
    filenames = ["a.pdf", "b.pdf"]

    vectordb.save_to_db(chunks, embeddings, filenames)
    loaded = vectordb.load_db()

    assert len(loaded) == 2
    assert loaded[0]["chunk"] == "chunk 1"
    assert loaded[1]["filename"] == "b.pdf"