import chromadb 
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

from backend.utils.logger import log

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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


def store_chunks(chunks,paper_title,source):

    for chunk in chunks:
        embedding = get_embedding(chunk.text)
        collection.add(
            ids=[f"{paper_title}_{chunk.chunk_id}"],
            documents=[chunk.text],
            embeddings=[embedding],
            metadatas=[
                {
                    "paper_title":paper_title,
                    "source":source,
                    "page_no":chunk.page_no,
                    "chunk_id":chunk.chunk_id
                }
            ]
        )
    log(f"Stored {len(chunks)} chunks")


def search_chunks(query,k=5):

    query_embedding = (
        get_embedding(query)
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    log(f"Retrieved {len(results)} chunks")

    results_list=[]

    for i in range(len(results["ids"][0])):
        metadata = results["metadatas"][0][i]
        results_list.append(
            {
                "paper_title":metadata["paper_title"],
                "source":metadata["source"],
                "page_no":metadata["page_no"],
                "chunk_id":metadata["chunk_id"],
                "text":results["documents"][0][i],
                "distance":results["distances"][0][i]
            }
        )
   
    return results_list


def retrieve_context(query,k=5):
    return search_chunks(query=query,k=k)