from backend.schemas.chunk import PDFChunk

## Chunker V1 - Text
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

## Chunker V2 - Page
def chunk_page(text,page_no,chunk_size=1000,overlap=200):

    chunks=[]
    start=0

    while start < len(text):

        end = start + chunk_size
        chunk_text = text[start:end]
        
        chunks.append(
            {
                "page_no":page_no,
                "text":chunk_text
            }
        )

        start += chunk_size - overlap
        
    return chunks

def build_chunks_from_pages(pages):

    chunks=[]
    chunk_id=0

    for page in pages:
        page_chunks = (chunk_page(
            page["text"],
            page["page_no"]
            )
        )

        for chunk in page_chunks:
            chunks.append(PDFChunk(
                chunk_id=chunk_id,
                page_no=chunk["page_no"],
                text=chunk["text"],
                length=len(chunk["text"])
                )
            )

            chunk_id += 1

    return chunks