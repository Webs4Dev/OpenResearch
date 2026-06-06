from backend.schemas.chunk import PDFChunk

def chunk_text(text:str,chunk_size:int=1000):
    chunks=[]

    for i in range(0,len(text),chunk_size):
        chunk=text[i:i+chunk_size]
        chunks.append(chunk)

    return chunks

def build_chunks(text:str,chunk_size:int=1000):
    
    raw_chunks = chunk_text(text,chunk_size)
    chunks = []

    for idx,chunk in enumerate(raw_chunks):
        chunks.append(PDFChunk(
            chunk_id=idx,
            text=chunk,
            length=len(chunk)
        ))
    
    return chunks