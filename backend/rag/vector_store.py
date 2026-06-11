import chromadb 
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KET")

client_db = chromadb.PersistentClient(path="./backend/rag/chroma_db")
client_openai = OpenAI(api_key=OPENAI_API_KEY)

collection = client_db.get_or_create_collection(
    name="papers"
)

def get_embedding(text):
    response = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def store_chunks(chunks,paper_name):

    for chunk in chunks:
        embedding = get_embedding(chunk.text)
        collection.add(
            ids=[f"{paper_name}_{chunk.chunk_id}"],
            documents=[chunk.text],
            embeddings=[embedding],
            metadatas=[
                {
                    "page":chunk.page_no
                }
            ]
        )

def search_chunks(query,k=5):

    query_embedding = (
        get_embedding(query)
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    
    return [
        {
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "page_no": results["metadatas"][0][i]["page"],
            "distance": results["distances"][0][i]
        }
        for i in range(
            len(results["ids"][0])
        )
    ]

