import fitz
from app.rag import ingest


def test_load_pdfs_ler_texto_real(tmp_path, monkeypatch):
    pdf_dir = tmp_path / "pdfs"
    pdf_dir.mkdir()

    pdf_path = pdf_dir / "sample.pdf"

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Regressao logistica e um metodo de classificacao.")
    doc.save(pdf_path)
    doc.close()

    monkeypatch.setattr(ingest, "PDF_FOLDER", pdf_dir)

    docs = ingest.load_pdfs()

    assert len(docs) == 1
    assert docs[0]["filename"] == "sample.pdf"
    assert "classificacao" in docs[0]["text"]