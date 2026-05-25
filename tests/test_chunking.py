from app.rag.chunking import split_text


def test_split_text_cria_chunks_com_overlap():
    texto = "0123456789" * 60
    chunks = split_text(texto, chunk_size=100, chunk_overlap=20)

    assert len(chunks) >= 2
    assert chunks[0][-20:] == chunks[1][:20]
    assert all(len(c) > 10 for c in chunks)