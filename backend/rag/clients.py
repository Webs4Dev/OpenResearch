import chromadb

client_db = chromadb.PersistentClient(path="./chroma_db")

chunk_collection = client_db.get_or_create_collection(
    name="pdf_chunks"
)
paper_collection = client_db.get_or_create_collection(
    name="paper_metadata"
)