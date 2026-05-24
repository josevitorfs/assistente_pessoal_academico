import os
import fitz

from app.rag.chunking import split_text
from app.rag.embeddings import generate_embeddings
from app.rag.vectordb import save_to_db

PDF_FOLDER = "data/pdfs"


def load_pdfs():
    documents = []
    
    if not os.path.exists(PDF_FOLDER):
        return documents

    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_FOLDER, filename)
            pdf_document = fitz.open(pdf_path)
            full_text = ""
            
            for page in pdf_document:
                full_text += page.get_text()
                
            documents.append({
                "filename": filename,
                "text": full_text
            })
            
    return documents


def run_ingestion():
    docs = load_pdfs()
    
    if not docs:
        print(f"Nenhum PDF encontrado em {PDF_FOLDER}.")
        return

    all_chunks = []
    all_filenames = []
    
    print(f"Iniciando processamento de {len(docs)} documentos...")
    for doc in docs:
        chunks = split_text(doc["text"])
        for chunk in chunks:
            all_chunks.append(chunk)
            all_filenames.append(doc["filename"])
                
    if not all_chunks:
        print("Nenhum fragmento de texto gerado.")
        return
        
    print(f"Gerando embeddings para {len(all_chunks)} chunks...")
    embeddings = generate_embeddings(all_chunks)
    
    save_to_db(all_chunks, embeddings, all_filenames)
    print("Ingestão concluída com sucesso!")


if __name__ == "__main__":
    run_ingestion()