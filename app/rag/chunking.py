def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 100) -> list:
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += (chunk_size - chunk_overlap)
        
    return [c for c in chunks if len(c) > 10]