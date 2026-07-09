import os
from openai import OpenAI
from dotenv import load_dotenv

from backend.utils.hash import generate_paper_id
load_dotenv()

from backend.utils.logger import log
from backend.rag.collection import chunk_collection

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client_openai = OpenAI(api_key=OPENAI_API_KEY)

def get_embedding(text):
    response = client_openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding

def is_paper_ingested(paper_title: str) -> bool:
    existing = chunk_collection.get(
        where={"paper_title": paper_title},
        limit=1
    )
    return len(existing["ids"]) > 0

def count_chunks_for_paper(paper_title: str) -> int:
    existing = chunk_collection.get(where={"paper_title": paper_title})
    return len(existing["ids"])

def store_chunks(chunks,paper_title):

    for chunk in chunks:
        embedding = get_embedding(chunk.text)
        chunk_code = generate_paper_id(f"{paper_title}_{chunk.chunk_id}")
        chunk_collection.add(
            ids=[chunk_code],
            documents=[chunk.text],
            embeddings=[embedding],
            metadatas=[
                {
                    "paper_title":paper_title,
                    "page_no":chunk.page_no,
                    "chunk_id":chunk.chunk_id
                }
            ]
        )
    log(f"Stored {len(chunks)} chunks")


def search_chunks(query,k=5,paper_title=None):

    query_embedding = get_embedding(query)
    if not paper_title:
        results = chunk_collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
    else:
        results = chunk_collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where={
                "paper_title":paper_title
            }
        )
    
    log(f"Retrieved {len(results["ids"][0])} chunks")

    results_list=[]

    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        relevance_score = round(1/(1+distance),3)*100

        metadata = results["metadatas"][0][i]
        results_list.append(
            {
                "paper_title":metadata["paper_title"],
                "url":metadata.get("url"),
                "year":metadata.get("year"),
                "page_no":metadata.get("page_no"),
                "chunk_id":metadata.get("chunk_id"),
                "text":results["documents"][0][i],
                "relevance_score":relevance_score
            }
        )
   
    return results_list


def retrieve_context(query,k=5):
    return search_chunks(query=query,k=k)


def format_chunks_context(chunks):
    context = ""

    for chunk in chunks:

        context += f"""
        PAPER: {chunk['paper_title']}
        SOURCE: {chunk['source']}
        TEXT:
        {chunk['text']}

        --------------------------------
        """

    return context